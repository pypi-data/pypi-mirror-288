from ..rpc_error import RPCError


class Forbidden(RPCError):
    CODE = 403
    """``int``: RPC Error Code"""
    NAME = __doc__


class BroadcastForbidden(Forbidden):
    ID = "BROADCAST_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChannelPublicGroupNa(Forbidden):
    ID = "CHANNEL_PUBLIC_GROUP_NA"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatAdminInviteRequired(Forbidden):
    ID = "CHAT_ADMIN_INVITE_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatAdminRequired(Forbidden):
    ID = "CHAT_ADMIN_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatForbidden(Forbidden):
    ID = "CHAT_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatGuestSendForbidden(Forbidden):
    ID = "CHAT_GUEST_SEND_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class EditBotInviteForbidden(Forbidden):
    ID = "EDIT_BOT_INVITE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class InlineBotRequired(Forbidden):
    ID = "INLINE_BOT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MessageAuthorRequired(Forbidden):
    ID = "MESSAGE_AUTHOR_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MessageDeleteForbidden(Forbidden):
    ID = "MESSAGE_DELETE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class NotAllowed(Forbidden):
    ID = "NOT_ALLOWED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class NotEligible(Forbidden):
    ID = "NOT_ELIGIBLE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ParticipantJoinMissing(Forbidden):
    ID = "PARTICIPANT_JOIN_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PollVoteRequired(Forbidden):
    ID = "POLL_VOTE_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PremiumAccountRequired(Forbidden):
    ID = "PREMIUM_ACCOUNT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PrivacyPremiumRequired(Forbidden):
    ID = "PRIVACY_PREMIUM_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PublicChannelMissing(Forbidden):
    ID = "PUBLIC_CHANNEL_MISSING"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class RightForbidden(Forbidden):
    ID = "RIGHT_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class SensitiveChangeForbidden(Forbidden):
    ID = "SENSITIVE_CHANGE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class TakeoutRequired(Forbidden):
    ID = "TAKEOUT_REQUIRED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserBotInvalid(Forbidden):
    ID = "USER_BOT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserChannelsTooMuch(Forbidden):
    ID = "USER_CHANNELS_TOO_MUCH"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserDeleted(Forbidden):
    ID = "USER_DELETED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserInvalid(Forbidden):
    ID = "USER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserIsBlocked(Forbidden):
    ID = "USER_IS_BLOCKED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserNotMutualContact(Forbidden):
    ID = "USER_NOT_MUTUAL_CONTACT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserPrivacyRestricted(Forbidden):
    ID = "USER_PRIVACY_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UserRestricted(Forbidden):
    ID = "USER_RESTRICTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendAudiosForbidden(Forbidden):
    ID = "CHAT_SEND_AUDIOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendDocsForbidden(Forbidden):
    ID = "CHAT_SEND_DOCS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendGameForbidden(Forbidden):
    ID = "CHAT_SEND_GAME_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendGifsForbidden(Forbidden):
    ID = "CHAT_SEND_GIFS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendInlineForbidden(Forbidden):
    ID = "CHAT_SEND_INLINE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendMediaForbidden(Forbidden):
    ID = "CHAT_SEND_MEDIA_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendPhotosForbidden(Forbidden):
    ID = "CHAT_SEND_PHOTOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendPlainForbidden(Forbidden):
    ID = "CHAT_SEND_PLAIN_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendPollForbidden(Forbidden):
    ID = "CHAT_SEND_POLL_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendStickersForbidden(Forbidden):
    ID = "CHAT_SEND_STICKERS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendVideosForbidden(Forbidden):
    ID = "CHAT_SEND_VIDEOS_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatSendVoicesForbidden(Forbidden):
    ID = "CHAT_SEND_VOICES_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatWriteForbidden(Forbidden):
    ID = "CHAT_WRITE_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class GroupcallAlreadyStarted(Forbidden):
    ID = "GROUPCALL_ALREADY_STARTED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class GroupcallForbidden(Forbidden):
    ID = "GROUPCALL_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class LiveDisabled(Forbidden):
    ID = "LIVE_DISABLED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatGuestSendForbidden(Forbidden):
    ID = "CHAT_GUEST_SEND_FORBIDDEN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
