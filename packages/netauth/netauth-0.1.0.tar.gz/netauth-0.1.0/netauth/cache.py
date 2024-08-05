import abc
from pathlib import Path
from tempfile import gettempdir

__all__ = [
    "TokenCache",
    "FSTokenCache",
    "MemoryTokenCache",
]


class TokenCache(abc.ABC):
    """
    Base class for token caches
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def put(self, entity: str, token: str):
        """
        Add or set the token for an entity

        :param entity: token's owner
        :param token: token to store
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, entity: str) -> str | None:
        """
        Get the token for an entity

        :param entity: token's owner
        :return: token, or ``None`` if not in cache
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, entity: str):
        """
        Remove the token for an entity

        :param entity: token's owner
        """
        raise NotImplementedError


class FSTokenCache(TokenCache):
    """
    Filesystem-backed token cache. Stores tokens in files named `{entity}.nt`
    in the OS's temporary files directory.

    Useful for short-running applications and prefetching tokens.
    """

    def __init__(self):
        self.__basedir = Path(gettempdir())
        self.__basedir.mkdir(mode=0o700, parents=True, exist_ok=True)

    def put(self, entity: str, token: str):
        p = self.__path_from_entity(entity)
        p.touch(mode=0o600, exist_ok=True)
        p.write_text(token)

    def get(self, entity: str) -> str | None:
        p = self.__path_from_entity(entity)
        try:
            return p.read_text()
        except FileNotFoundError:
            return None

    def delete(self, entity: str):
        p = self.__path_from_entity(entity)
        p.unlink(missing_ok=True)

    def __path_from_entity(self, entity: str) -> Path:
        return self.__basedir / f"{entity}.nt"


class MemoryTokenCache(TokenCache):
    """
    Memory-backed token cache. Stores tokens in a mapping that lasts as long as
    the object.

    Useful for applications like web interfaces.
    """

    def __init__(self):
        self.__cache: dict[str, str] = {}

    def put(self, entity: str, token: str):
        self.__cache[entity] = token

    def get(self, entity: str) -> str | None:
        try:
            return self.__cache[entity]
        except KeyError:
            return None

    def delete(self, entity: str):
        try:
            del self.__cache[entity]
        except KeyError:
            pass
