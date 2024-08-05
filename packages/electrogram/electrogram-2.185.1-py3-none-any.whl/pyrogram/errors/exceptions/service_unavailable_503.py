from ..rpc_error import RPCError


class ServiceUnavailable(RPCError):
    CODE = 503
    """``int``: RPC Error Code"""
    NAME = __doc__


class ApiCallError(ServiceUnavailable):
    ID = "ApiCallError"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class Timeout(ServiceUnavailable):
    ID = "Timeout"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class Timedout(ServiceUnavailable):
    ID = "Timedout"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
