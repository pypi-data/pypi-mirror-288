from ..rpc_error import RPCError


class InternalServerError(RPCError):
    CODE = 500
    """``int``: RPC Error Code"""
    NAME = __doc__


class ApiCallError(InternalServerError):
    ID = "API_CALL_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class AuthRestart(InternalServerError):
    ID = "AUTH_RESTART"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class CallOccupyFailed(InternalServerError):
    ID = "CALL_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatIdGenerateFailed(InternalServerError):
    ID = "CHAT_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatOccupyLocFailed(InternalServerError):
    ID = "CHAT_OCCUPY_LOC_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatOccupyUsernameFailed(InternalServerError):
    ID = "CHAT_OCCUPY_USERNAME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChpCallFail(InternalServerError):
    ID = "CHP_CALL_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class EncryptionOccupyAdminFailed(InternalServerError):
    ID = "ENCRYPTION_OCCUPY_ADMIN_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class EncryptionOccupyFailed(InternalServerError):
    ID = "ENCRYPTION_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class FolderDeacAutofixAll(InternalServerError):
    ID = "FOLDER_DEAC_AUTOFIX_ALL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class GroupcallAddParticipantsFailed(InternalServerError):
    ID = "GROUPCALL_ADD_PARTICIPANTS_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class GroupedIdOccupyFailed(InternalServerError):
    ID = "GROUPED_ID_OCCUPY_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class HistoryGetFailed(InternalServerError):
    ID = "HISTORY_GET_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ImageEngineDown(InternalServerError):
    ID = "IMAGE_ENGINE_DOWN"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class InterdcCallError(InternalServerError):
    ID = "INTERDC_X_CALL_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class InterdcCallRichError(InternalServerError):
    ID = "INTERDC_X_CALL_RICH_ERROR"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MemberFetchFailed(InternalServerError):
    ID = "MEMBER_FETCH_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MemberNoLocation(InternalServerError):
    ID = "MEMBER_NO_LOCATION"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MemberOccupyPrimaryLocFailed(InternalServerError):
    ID = "MEMBER_OCCUPY_PRIMARY_LOC_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MemberOccupyUsernameFailed(InternalServerError):
    ID = "MEMBER_OCCUPY_USERNAME_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MsgidDecreaseRetry(InternalServerError):
    ID = "MSGID_DECREASE_RETRY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MsgRangeUnsync(InternalServerError):
    ID = "MSG_RANGE_UNSYNC"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class MtSendQueueTooLong(InternalServerError):
    ID = "MT_SEND_QUEUE_TOO_LONG"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class NeedChatInvalid(InternalServerError):
    ID = "NEED_CHAT_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class NeedMemberInvalid(InternalServerError):
    ID = "NEED_MEMBER_INVALID"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class NoWorkersRunning(InternalServerError):
    ID = "No workers running"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ParticipantCallFailed(InternalServerError):
    ID = "PARTICIPANT_CALL_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PersistentTimestampOutdated(InternalServerError):
    ID = "PERSISTENT_TIMESTAMP_OUTDATED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PhotoCreateFailed(InternalServerError):
    ID = "PHOTO_CREATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PostponedTimeout(InternalServerError):
    ID = "POSTPONED_TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class PtsChangeEmpty(InternalServerError):
    ID = "PTS_CHANGE_EMPTY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class RandomIdDuplicate(InternalServerError):
    ID = "RANDOM_ID_DUPLICATE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class RegIdGenerateFailed(InternalServerError):
    ID = "REG_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class RpcCallFail(InternalServerError):
    ID = "RPC_CALL_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class RpcConnectFailed(InternalServerError):
    ID = "RPC_CONNECT_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class RpcMcgetFail(InternalServerError):
    ID = "RPC_MCGET_FAIL"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class SignInFailed(InternalServerError):
    ID = "SIGN_IN_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class StorageCheckFailed(InternalServerError):
    ID = "STORAGE_CHECK_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class StoreInvalidScalarType(InternalServerError):
    ID = "STORE_INVALID_SCALAR_TYPE"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class Timeout(InternalServerError):
    ID = "TIMEOUT"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UnknownMethod(InternalServerError):
    ID = "UNKNOWN_METHOD"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class UploadNoVolume(InternalServerError):
    ID = "UPLOAD_NO_VOLUME"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class VolumeLocNotFound(InternalServerError):
    ID = "VOLUME_LOC_NOT_FOUND"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class WorkerBusyTooLongRetry(InternalServerError):
    ID = "WORKER_BUSY_TOO_LONG_RETRY"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class WpIdGenerateFailed(InternalServerError):
    ID = "WP_ID_GENERATE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class FileWriteFailed(InternalServerError):
    ID = "FILE_WRITE_FAILED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
class ChatFromCallChanged(InternalServerError):
    ID = "CHAT_FROM_CALL_CHANGED"
    """``str``: RPC Error ID"""
    MESSAGE = __doc__
