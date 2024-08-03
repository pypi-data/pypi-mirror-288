from ..rpc_error import RPCError


class NotAcceptable(RPCError):
    CODE = 406
    """``int``: RPC Error Code"""
    NAME = __doc__


class AuthKeyDuplicated(NotAcceptable):
    ID = "AUTH_KEY_DUPLICATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChannelPrivate(NotAcceptable):
    ID = "CHANNEL_PRIVATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChannelTooLarge(NotAcceptable):
    ID = "CHANNEL_TOO_LARGE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatForwardsRestricted(NotAcceptable):
    ID = "CHAT_FORWARDS_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class FilerefUpgradeNeeded(NotAcceptable):
    ID = "FILEREF_UPGRADE_NEEDED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class FreshChangeAdminsForbidden(NotAcceptable):
    ID = "FRESH_CHANGE_ADMINS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class FreshChangePhoneForbidden(NotAcceptable):
    ID = "FRESH_CHANGE_PHONE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class FreshResetAuthorisationForbidden(NotAcceptable):
    ID = "FRESH_RESET_AUTHORISATION_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class GiftcodeNotAllowed(NotAcceptable):
    ID = "GIFTCODE_NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class InviteHashExpired(NotAcceptable):
    ID = "INVITE_HASH_EXPIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PhoneNumberInvalid(NotAcceptable):
    ID = "PHONE_NUMBER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PhonePasswordFlood(NotAcceptable):
    ID = "PHONE_PASSWORD_FLOOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PremiumCurrentlyUnavailable(NotAcceptable):
    ID = "PREMIUM_CURRENTLY_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PreviousChatImportActiveWaitMin(NotAcceptable):
    ID = "PREVIOUS_CHAT_IMPORT_ACTIVE_WAIT_XMIN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class SendCodeUnavailable(NotAcceptable):
    ID = "SEND_CODE_UNAVAILABLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class StickersetInvalid(NotAcceptable):
    ID = "STICKERSET_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class StickersetOwnerAnonymous(NotAcceptable):
    ID = "STICKERSET_OWNER_ANONYMOUS"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UpdateAppToLogin(NotAcceptable):
    ID = "UPDATE_APP_TO_LOGIN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserpicPrivacyRequired(NotAcceptable):
    ID = "USERPIC_PRIVACY_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserpicUploadRequired(NotAcceptable):
    ID = "USERPIC_UPLOAD_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserRestricted(NotAcceptable):
    ID = "USER_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
