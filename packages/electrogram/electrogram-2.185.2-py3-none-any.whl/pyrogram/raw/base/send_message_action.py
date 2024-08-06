from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SendMessageAction = Union["raw.types.SendMessageCancelAction", "raw.types.SendMessageChooseContactAction", "raw.types.SendMessageChooseStickerAction", "raw.types.SendMessageEmojiInteraction", "raw.types.SendMessageEmojiInteractionSeen", "raw.types.SendMessageGamePlayAction", "raw.types.SendMessageGeoLocationAction", "raw.types.SendMessageHistoryImportAction", "raw.types.SendMessageRecordAudioAction", "raw.types.SendMessageRecordRoundAction", "raw.types.SendMessageRecordVideoAction", "raw.types.SendMessageTypingAction", "raw.types.SendMessageUploadAudioAction", "raw.types.SendMessageUploadDocumentAction", "raw.types.SendMessageUploadPhotoAction", "raw.types.SendMessageUploadRoundAction", "raw.types.SendMessageUploadVideoAction", "raw.types.SpeakingInGroupCallAction"]


# noinspection PyRedeclaration
class SendMessageAction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SendMessageAction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
