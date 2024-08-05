import socket
from pathlib import Path
from collections.abc import Callable

import grpc
import tomllib

from . import _pb, v2, cache, error
from ._kv import (
    KVDict,
    from_KVData,
    parse_KVDict,
    to_KVValue,
)
from ._types import (
    Capability,
    Entity,
    EntityMeta,
    ExpansionMode,
    Group,
)

__all__ = [
    "NetAuth",
    "Capability",
    "Entity",
    "EntityMeta",
    "ExpansionMode",
    "Group",
    "KVDict",
    "v2",
    "cache",
    "error",
]

__version__ = "0.1.0"


class NetAuth:
    """
    Creates a new NetAuth client, connected and ready to use. If called as a
    context manager, the connection will automatically be closed upon exit.

    :param server: server to connect to
    :param port: port to connect to (default: ``1729``)
    :param master: the controller server in a NetAuth cluster (default: server)

    :param entity: the entity to perform authenticated operations as
    :param secret: entity's secret, or a callback for retrieving the entity's secret
    :param token_cache: a :class:`TokenCache` to store tokens in. If not specified,
        uses :class:`MemoryTokenCache`.

    :param client_name: value to identify the client by (default: hostname)
    :param service_name: value to identify the application or service by
        (default: ``"netauth-python"``)

    :param cert: TLS certificate to use (path to a PEM-encoded certificate,
        byte string of the PEM-encoded certificate itself, or ``None``
        (default) to retrieve them from the default location chosen by the
        gRPC runtime)
    :param insecure: disable TLS (default: ``False``)

    :raises NetAuthException: if ``server`` is not set
    """

    def __init__(
        self,
        server: str,
        port: int = 1729,
        *,
        master: str | None = None,
        entity: str | None = None,
        secret: str | Callable[[], str] | None = None,
        token_cache: cache.TokenCache | None = None,
        client_name: str | None = None,
        service_name: str | None = None,
        cert: Path | bytes | None = None,
        insecure: bool = False,
    ):
        self.server = server
        if not self.server:
            raise error.NetAuthException("invalid server")
        self.port = port
        self.master = master or server
        self.writable = self.server == self.master

        self.entity = entity
        self.__secret = secret
        self.cache = token_cache or cache.MemoryTokenCache()

        # seems very unlikely to error, but possible
        # CPython is inscrutable about what the exception could be
        try:
            self.client_name = client_name or socket.gethostname()
        except:  # noqa: E722
            self.client_name = "BOGUS_CLIENT"
        self.service_name = service_name or "netauth-python"

        self.insecure = insecure

        if not insecure:
            if isinstance(cert, Path):
                with cert.open("rb") as cf:
                    cert = cf.read()
            self.credentials = grpc.ssl_channel_credentials(root_certificates=cert)
        else:
            self.credentials = None

        self.__connect()

    @classmethod
    def with_config(cls, path: Path, **kwargs):
        """
        Creates a new NetAuth client, connected and ready to use, from a NetAuth
        configuration file. This should be a TOML file with the same format as
        the NetAuth commandline utility's configuration.

        Accepts the same arguments as ``__init__`` as keyword arguments. If
        specified, they will override values from the configuration.

        :param path: path to the configuration file
        """
        with path.open("rb") as f:
            cfg = tomllib.load(f)

        core = cfg.get("core", {})
        client = cfg.get("client", {})
        tls = cfg.get("tls", {})
        token = cfg.get("token", {})

        cert = Path(tls.get("certificate", "keys/tls.pem"))
        if not cert.is_absolute():
            cert = (path.parent / cert).absolute()

        match token.get("cache"):
            case "fs":
                tcache = cache.FSTokenCache()
            case "memory":
                tcache = cache.MemoryTokenCache()
            case _:
                tcache = None

        args = {
            "server": core.get("server"),
            "port": core.get("port", 1729),
            "master": core.get("master"),
            "token_cache": tcache,
            "client_name": client.get("ID"),
            "cert": cert,
            "insecure": tls.get("pwn_me", False),
        }
        args.update(kwargs)

        return cls(**args)

    def __connect(self, writable: bool = False):
        if writable:
            server = self.master
        else:
            server = self.server
        target = f"{server}:{self.port}"

        if self.insecure:
            self.channel = grpc.insecure_channel(target)
        else:
            self.channel = grpc.secure_channel(target, self.credentials)

        self.stub = _pb.v2.NetAuth2Stub(self.channel)

    def close(self):
        """
        Close the underlying gRPC connection. Called automatically when the
        client object is deleted or, when using a context manager, the context
        is left.
        """
        self.channel.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.close()

    def __del__(self):
        try:
            self.close()
        except:  # noqa: E722
            pass

    def __make_writable(self):
        """Reconnect to the master server in the cluster if not already"""
        if not (self.server == self.master or self.writable):
            self.__connect(True)
            self.writable = True

    def __metadata(self, *, auth: bool) -> list[tuple[str, str]]:
        """
        Generate metadata for an RPC request.

        :param auth: whether to include the authorization header (default: ``False``)
        :return: the metadata for the request
        """
        meta = [
            ("client-name", self.client_name),
            ("service-name", self.service_name),
        ]
        if auth:
            meta.append(("authorization", self.token))
        return meta

    @property
    def secret(self) -> str:
        if not self.__secret:
            raise error.NetAuthException("secret not set")
        if isinstance(self.__secret, Callable):
            return self.__secret()
        return self.__secret

    @secret.setter
    def secret(self, value: str | Callable[[], str]):
        self.__secret = value

    @secret.deleter
    def secret(self):
        self.__secret = None

    def __refresh_token(self) -> str:
        if not self.entity:
            raise error.NetAuthException("cannot refresh token without an entity")
        token = self.auth_get_token(self.entity, self.secret)
        self.cache.put(self.entity, token)
        return token

    @property
    def token(self) -> str:
        if not self.entity:
            raise error.NetAuthException("cannot perform authenticated actions without an entity")

        if (token := self.cache.get(self.entity)) is None:
            token = self.__refresh_token()
        else:
            try:
                self.auth_validate_token(token)
            except error.UnauthenticatedError:
                token = self.__refresh_token()

        return token

    def entity_create(self, id: str, secret: str, number: int = -1):
        """
        Create a new entity.

        :param id: the new entity's ID. Must be unique.
        :param secret: the new entity's secret.
        :param number: the new entity's number. Strongly recommended to be unique.
            If not provided, the next valid number will be selected and assigned.
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises ExistsError: if the entity ID or number already exists
        :raises InternalError: if some other error occurred during creation
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.EntityCreate(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(
                        ID=id,
                        secret=secret,
                        Number=number,
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_update(self, id: str, meta: EntityMeta):
        """
        Update the generic metadata on an existing entity.

        :param id: the entity's ID
        :param meta: the new metadata values
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during update
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.EntityUpdate(
                request=_pb.v2.EntityRequest(
                    Data=_pb.Entity(
                        ID=id,
                        meta=meta._into(),
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_info(self, id: str) -> Entity | None:
        """
        Returns information about an entity. Does not require authentication.

        :param id: the entity's ID
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: the entity or ``None`` if not found
        """
        try:
            resp: _pb.v2.ListOfEntities = self.stub.EntityInfo(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(
                        ID=id,
                    ),
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if resp.Entities:
            return Entity._from(resp.Entities[0])

    def entity_search(self, expr: str) -> list[Entity]:
        """
        Searches all entities. Does not require authentication.

        :param expr: expression to search for
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: list of entities that match the search criteria
        """
        try:
            resp: _pb.v2.ListOfEntities = self.stub.EntitySearch(
                request=_pb.v2.SearchRequest(expression=expr),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if resp.Entities is not None:
            return [Entity._from(e) for e in resp.Entities]
        return []

    def entity_untyped_meta(self, id: str, action: v2.Action, key: str, value: str = "") -> KVDict | None:
        """
        Perform operations on the untyped key-value store on an entity. Read
        operations do not require authentication.

        :param id: target entity ID
        :param action: action to perform (``Upsert``, ``Read``, ``ClearFuzzy``, or ``ClearExact``)
        :param key: key to read from or write to. If ``'*'``, operate on all keys.
        :param value: value to write, if writing
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided or an invalid :class:`Action` was given
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: a dictionary of the requested keys and values if reading, nothing if writing or clearing
        """
        auth = False
        if action != v2.Action.Read:
            self.__make_writable()
            auth = True

        try:
            resp: _pb.v2.ListOfStrings = self.stub.EntityUM(
                request=_pb.v2.KVRequest(
                    Target=id,
                    Action=action._into(),
                    Key=key,
                    Value=value,
                ),
                metadata=self.__metadata(auth=auth),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if action == v2.Action.Read:
            kv = parse_KVDict(list(resp.Strings))
            if key != "*":
                return {key: kv[key]}
            return kv

    def entity_kv_add(self, id: str, key: str, values: list[str]):
        """
        Add a key to the specified entity. The key must not already exist.
        Value order will be preserved.

        :param id: target entity ID
        :param key: the key to add
        :param values: the values to add
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises ExistsError: if the key already exists
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        vals = [to_KVValue(v, i) for i, v in enumerate(values)]

        try:
            self.stub.EntityKVAdd(
                request=_pb.v2.KV2Request(
                    Target=id,
                    Data=_pb.KVData(
                        Key=key,
                        Values=vals,
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            e = error.from_RpcError(e)
            if e:
                raise e

    def entity_kv_get(self, id: str, key: str) -> KVDict:
        """
        Returns values for the requested key if it exists.

        :param id: target entity ID
        :param key: the key to retrieve. If ``'*'``, get all keys.
        :raises DoesNotExistError: if the entity or key does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: the key-value mapping requested
        """
        try:
            resp: _pb.v2.ListOfKVData = self.stub.EntityKVGet(
                request=_pb.v2.KV2Request(
                    Target=id,
                    Data=_pb.KVData(Key=key),
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        return from_KVData(list(resp.KVData))

    def entity_kv_del(self, id: str, key: str):
        """
        Delete a key from an entity.

        :param id: target entity ID
        :param key: the key to delete
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity or key does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.EntityKVDel(
                request=_pb.v2.KV2Request(
                    Target=id,
                    Data=_pb.KVData(Key=key),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_kv_replace(self, id: str, key: str, values: list[str]):
        """
        Replace a key for the specified entity. The key must already exist.
        Value order will be preserved.

        :param id: target entity ID
        :param key: the key to replace
        :param values: the values to add
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity or key does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        vals = [to_KVValue(v, i) for i, v in enumerate(values)]

        try:
            self.stub.EntityKVReplace(
                request=_pb.v2.KV2Request(
                    Target=id,
                    Data=_pb.KVData(
                        Key=key,
                        Values=vals,
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_keys(self, id: str, action: v2.Action, kind: str, key: str) -> KVDict | None:
        """
        Read, write, or drop public keys stored on an entity. Does not require authentication.

        :param id: target entity ID
        :param action: action to perform (``Add``, ``Drop``, or ``Read``)
        :param kind: type of key. If ``'*'``, operate on all key types.
        :param key: key value
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided or an invalid :class:`Action` was given
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: a dictionary of the requested keys and values if reading, nothing if writing or clearing
        """
        auth = False
        if action != v2.Action.Read:
            self.__make_writable()
            auth = True

        try:
            resp: _pb.v2.ListOfStrings = self.stub.EntityKeys(
                request=_pb.v2.KVRequest(
                    Target=id,
                    Action=action._into(),
                    Key=kind,
                    Value=key,
                ),
                metadata=self.__metadata(auth=auth),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if action == v2.Action.Read:
            kv = parse_KVDict(list(resp.Strings))
            if key != "*":
                return {kind: kv[kind]}
            return kv

    def entity_destroy(self, id: str):
        """
        Permanently remove an entity from the server.This is not recommended
        and should not be done without good reason. The best practice is to
        instead have a group that defunct entities get moved to and then locked.
        This will prevent authentication, while maintaining integrity of the
        backing tree. This function does not maintain referential integrity, so
        be careful about removing the last standing admin of a particular type.

        :param id: target entity ID
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.EntityDestroy(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(ID=id),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_lock(self, id: str):
        """
        Sets the lock bit on the target entity. Prevents authentication from
        proceeding even if correct authentication information is provided.

        :param id: target entity ID
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.EntityLock(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(ID=id),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_unlock(self, id: str):
        """
        Unsets the lock bit on the target entity.

        :param id: target entity ID
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.EntityUnlock(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(ID=id),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def entity_groups(self, id: str) -> list[Group]:
        """
        Retrieves the effective group memberships of the target entity.

        :param id: target entity ID
        :raises DoesNotExistError: if the entity does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        try:
            resp: _pb.v2.ListOfGroups = self.stub.EntityGroups(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(ID=id),
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        return [Group._from(g) for g in resp.Groups]

    def auth_entity(self, id: str, secret: str):
        """
        Perform authentication for an entity. Does not acquire a token.

        :param id: target entity ID
        :param secret: target entity's secret
        :raises UnauthenticatedError: if authentication failed
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        try:
            self.stub.AuthEntity(
                request=_pb.v2.AuthRequest(
                    Entity=_pb.Entity(ID=id),
                    Secret=secret,
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def auth_get_token(self, id: str, secret: str) -> str:
        """
        Perform authentication for an entity and acquire a token if successful.
        This token can be used to authenticate future requests.

        :param id: target entity ID
        :param secret: target entity's secret
        :raises UnauthenticatedError: if authentication failed
        :raises InternalError: if an error occurred while issuing a token
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: token, if successful
        """
        try:
            resp: _pb.v2.AuthResult = self.stub.AuthGetToken(
                request=_pb.v2.AuthRequest(
                    Entity=_pb.Entity(ID=id),
                    Secret=secret,
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        return resp.Token

    def auth_validate_token(self, token: str):
        """
        Perform server-side validation of a token.

        :param token: token to check
        :raises UnauthenticatedError: if validation failed
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        try:
            self.stub.AuthValidateToken(
                request=_pb.v2.AuthRequest(Token=token),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def auth_change_secret(self, id: str, secret: str, old_secret: str | None = None):
        """
        Change the secret for an entity. If the entity is changing its own
        secret, the old secret should be provided. If an administrator is
        changing the secret, the request must be authenticated with a token.

        :param id: target entity ID
        :param secret: target entity's new secret
        :param old_secret: target entity's current secret, if needed
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid or (when changing its own secret)
            if ``old_secret`` was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.AuthChangeSecret(
                request=_pb.v2.AuthRequest(
                    Entity=_pb.Entity(
                        ID=id,
                        secret=old_secret,
                    ),
                    Secret=secret,
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_create(self, name: str, display_name: str, managed_by: str | None = None, number: int = -1):
        """
        Create a new group.

        :param name: new group's name. Must be unique.
        :param display_name: the new group's display name.
        :param managed_by: the name of a group that manages the new group
        :param number: the new group's number. Strongly recommended to be unique.
            If not provided, the next valid number will be selected and assigned.
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises ExistsError: if the group name or number already exists
        :raises InternalError: if some other error occurred during creation
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupCreate(
                request=_pb.v2.GroupRequest(
                    Group=_pb.Group(
                        Name=name,
                        DisplayName=display_name,
                        ManagedBy=managed_by,
                        Number=number,
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_update(self, group: Group):
        """
        Update group information. Fields that cannot be rewritten will be ignored.

        :param group: new group information
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group does not exist
        :raises InternalError: if some other error occurred during update
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupUpdate(
                request=_pb.v2.GroupRequest(
                    Group=group._into(),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_info(self, name: str) -> tuple[Group, list[Group]] | None:
        """
        Returns information about a group. Does not require authentication.

        :param name: target group's name
        :raises DoesNotExistError: if the group does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: a tuple of the group and its managed groups, if found
        """
        try:
            resp: _pb.v2.ListOfGroups = self.stub.GroupInfo(
                request=_pb.v2.GroupRequest(
                    Group=_pb.Group(Name=name),
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if resp.Groups:
            group = Group._from(resp.Groups[0])

            try:
                managed = self.group_search(f"ManagedBy:{name}")
            except error.NetAuthRpcError:
                # assume error = no managed groups
                managed = []

            return (group, managed)

    def group_untyped_meta(self, name: str, action: v2.Action, key: str, value: str = "") -> KVDict | None:
        """
        Perform operations on the untyped key-value store on a group. Read
        operations do not require authentication.

        :param name: target group's name
        :param action: action to perform (``Upsert``, ``Read``, ``ClearFuzzy``, or ``ClearExact``)
        :param key: key to read from or write to. If ``'*'``, operate on all keys.
        :param value: value to write, if writing
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided or an invalid :class:`Action` was given
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: a dictionary of the requested keys and values if reading, nothing if writing or clearing
        """
        auth = False
        if action != v2.Action.Read:
            self.__make_writable()
            auth = True

        try:
            resp: _pb.v2.ListOfStrings = self.stub.GroupUM(
                request=_pb.v2.KVRequest(
                    Target=name,
                    Action=action._into(),
                    Key=key,
                    Value=value,
                ),
                metadata=self.__metadata(auth=auth),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if action == v2.Action.Read:
            kv = parse_KVDict(list(resp.Strings))
            if key != "*":
                return {key: kv[key]}
            return kv

    def group_kv_add(self, name: str, key: str, values: list[str]):
        """
        Add a key to the specified group. The key must not already exist.
        Value order will be preserved.

        :param name: target group name
        :param key: the key to add
        :param values: the values to add
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group does not exist
        :raises ExistsError: if the key already exists (NetAuth >0.6.1)
        :raises InternalError: if the key already exists (NetAuth <=0.6.1) or some other error occurred
            during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        vals = [to_KVValue(v, i) for i, v in enumerate(values)]

        try:
            self.stub.GroupKVAdd(
                request=_pb.v2.KV2Request(
                    Target=name,
                    Data=_pb.KVData(
                        Key=key,
                        Values=vals,
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_kv_get(self, name: str, key: str) -> KVDict:
        """
        Returns values for the requested key if it exists.

        :param name: target group name
        :param key: the key to retrieve. If ``'*'``, get all keys.
        :raises DoesNotExistError: if the group or key does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: the key-value mapping requested
        """
        try:
            resp: _pb.v2.ListOfKVData = self.stub.GroupKVGet(
                request=_pb.v2.KV2Request(
                    Target=name,
                    Data=_pb.KVData(Key=key),
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        return from_KVData(list(resp.KVData))

    def group_kv_del(self, name: str, key: str):
        """
        Delete a key from a group.

        :param name: target group name
        :param key: the key to delete
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group or key does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupKVDel(
                request=_pb.v2.KV2Request(
                    Target=name,
                    Data=_pb.KVData(Key=key),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_kv_replace(self, name: str, key: str, values: list[str]):
        """
        Replace a key for the specified group. The key must already exist.
        Value order will be preserved.

        :param name: target group name
        :param key: the key to replace
        :param values: the values to add
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group or key does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        vals = [to_KVValue(v, i) for i, v in enumerate(values)]

        try:
            self.stub.GroupKVReplace(
                request=_pb.v2.KV2Request(
                    Target=name,
                    Data=_pb.KVData(
                        Key=key,
                        Values=vals,
                    ),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_update_rules(self, name: str, action: v2.RuleAction, target: str):
        """
        Manage rules on groups. Rules can an transparently include other groups,
        recursively remove members, or reset the behavior of a group to default.

        :param name: group name
        :param action: type of rule action to take
        :param target: target group name
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupUpdateRules(
                request=_pb.v2.GroupRulesRequest(
                    Group=_pb.Group(Name=name),
                    Target=_pb.Group(Name=target),
                    RuleAction=action._into(),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_add_member(self, group: str, entity: str):
        """
        Add a member to a group.

        :param group: target group name
        :param entity: ID of the entity to add
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupAddMember(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(ID=entity, meta=_pb.EntityMeta(Groups=[group])),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_del_member(self, group: str, entity: str):
        """
        Remove a member from a group.

        :param group: target group name
        :param entity: ID of the entity to remove
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupDelMember(
                request=_pb.v2.EntityRequest(
                    Entity=_pb.Entity(ID=entity, meta=_pb.EntityMeta(Groups=[group])),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_destroy(self, name: str):
        """
        Permanently remove a group from the server. This is not recommended as
        NetAuth does not perform internal referential integrity checks, so it
        is possible to remove a group that has rules pointing at it or
        otherwise create cycles in the graph. The best practices are to keep
        groups forever. They're cheap and as long as they're not queried they
        don't represent additional load.

        :param name: target group name
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises DoesNotExistError: if the group does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.GroupDestroy(
                request=_pb.v2.GroupRequest(
                    Group=_pb.Group(Name=name),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def group_members(self, name: str) -> list[Entity]:
        """
        Returns the membership of a group, include any alterations from rules.

        :param name: the name of the group
        :raises DoesNotExistError: if the group does not exist
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: the group members
        """
        try:
            resp: _pb.v2.ListOfEntities = self.stub.GroupMembers(
                request=_pb.v2.GroupRequest(
                    Group=_pb.Group(Name=name),
                ),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        return [Entity._from(e) for e in resp.Entities]

    def group_search(self, expr: str) -> list[Group]:
        """
        Searches all groups. Does not require authentication.

        :param expr: expression to search for
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        :return: list of groups that match the search criteria
        """
        try:
            resp: _pb.v2.ListOfGroups = self.stub.GroupSearch(
                request=_pb.v2.SearchRequest(expression=expr),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        if resp.Groups is not None:
            return [Group._from(e) for e in resp.Groups]
        return []

    def system_capabilities(self, target: str, action: v2.Action, capability: Capability, direct: bool = False):
        """
        Modify capabilities within the server.

        :param target: name of group or ID of entity to set the capability on
        :param action: action to perform (``Add`` or ``Drop``)
        :param capability: capability to add or drop
        :param direct: set the capability on an entity ``target`` (discouraged,
            default: ``False``)
        :raises ReadOnlyError: if the server is read-only
        :raises MalformedRequestError: if a token was not provided or an invalid :class:`Action` was given
        :raises UnauthenticatedError: if the token was not valid
        :raises RequestorUnqualifiedError: if the requestor does not have the necessary capabilities
        :raises InternalError: if some other error occurred during the request
        :raises NetAuthRpcError: if a gRPC error occurred
        """
        self.__make_writable()

        try:
            self.stub.SystemCapabilities(
                request=_pb.v2.CapabilityRequest(
                    Direct=direct,
                    Target=target,
                    Action=action._into(),
                    Capability=capability._into(),
                ),
                metadata=self.__metadata(auth=True),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def system_ping(self):
        """
        Pings the server. Returns successfully if the server is healthy.

        :raises NetAuthRpcError: if a gRPC error occurred
        """
        try:
            self.stub.SystemPing(
                request=_pb.v2.Empty(),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

    def system_status(self) -> v2.ServerStatus:
        """
        Returns detailed status information about the server.

        :raises NetAuthRpcError: if a gRPC error occurred
        :return: server status information
        """
        try:
            resp: _pb.v2.ServerStatus = self.stub.SystemStatus(
                request=_pb.v2.Empty(),
                metadata=self.__metadata(auth=False),
            )
        except grpc.RpcError as e:
            err = error.from_RpcError(e)
            raise err from e if type(err) is error.NetAuthRpcError else None

        return v2.ServerStatus._from(resp)
