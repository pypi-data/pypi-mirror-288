from ..rpc_error import RPCError


class Unauthorized(RPCError):
    CODE = 401
    """``int``: RPC Error Code"""
    NAME = __doc__


class ActiveUserRequired(Unauthorized):
    ID = "ACTIVE_USER_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class AuthKeyInvalid(Unauthorized):
    ID = "AUTH_KEY_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class AuthKeyPermEmpty(Unauthorized):
    ID = "AUTH_KEY_PERM_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class AuthKeyUnregistered(Unauthorized):
    ID = "AUTH_KEY_UNREGISTERED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class SessionExpired(Unauthorized):
    ID = "SESSION_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class SessionPasswordNeeded(Unauthorized):
    ID = "SESSION_PASSWORD_NEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class SessionRevoked(Unauthorized):
    ID = "SESSION_REVOKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserDeactivated(Unauthorized):
    ID = "USER_DEACTIVATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserDeactivatedBan(Unauthorized):
    ID = "USER_DEACTIVATED_BAN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
