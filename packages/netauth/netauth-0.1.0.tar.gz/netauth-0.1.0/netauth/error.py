import grpc

__all__ = [
    "NetAuthException",
    "NetAuthRpcError",
    "RequestorUnqualifiedError",
    "MalformedRequestError",
    "InternalError",
    "UnauthenticatedError",
    "ReadOnlyError",
    "ExistsError",
    "DoesNotExistError",
]


class NetAuthException(Exception):
    """Base class for exceptions raised by `netauth`"""

    def __init__(self, details: str, *args) -> None:
        self.details = details
        super().__init__(*args)

    def __str__(self) -> str:
        return self.details


class NetAuthRpcError(NetAuthException):
    """Base class for exceptions originating from the NetAuth server"""

    def __init__(self, details: str, code: grpc.StatusCode, *args) -> None:
        self.code = code
        super().__init__(details, *args)

    def __str__(self) -> str:
        return f"{self.details} ({self.code.name})"


class RequestorUnqualifiedError(NetAuthRpcError):
    pass


class MalformedRequestError(NetAuthRpcError):
    pass


class InternalError(NetAuthRpcError):
    pass


class UnauthenticatedError(NetAuthRpcError):
    pass


class ReadOnlyError(NetAuthRpcError):
    pass


class ExistsError(NetAuthRpcError):
    pass


class DoesNotExistError(NetAuthRpcError):
    pass


def from_RpcError(err: grpc.RpcError) -> NetAuthRpcError:
    # grpc.RpcError is also a grpc.Call, so we can "convert" it
    err_call: grpc.Call = err  # type: ignore
    code = err_call.code()
    details = err_call.details()
    match code:
        case grpc.StatusCode.PERMISSION_DENIED:
            return RequestorUnqualifiedError(details, code)
        case grpc.StatusCode.INVALID_ARGUMENT:
            return MalformedRequestError(details, code)
        case grpc.StatusCode.INTERNAL:
            return InternalError(details, code)
        case grpc.StatusCode.UNAUTHENTICATED:
            return UnauthenticatedError(details, code)
        case grpc.StatusCode.UNIMPLEMENTED:
            return ReadOnlyError(details, code)
        case grpc.StatusCode.ALREADY_EXISTS:
            return ExistsError(details, code)
        case grpc.StatusCode.NOT_FOUND:
            return DoesNotExistError(details, code)
        case _:
            return NetAuthRpcError(details, code)
