from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessagesFilter = Union["raw.types.InputMessagesFilterChatPhotos", "raw.types.InputMessagesFilterContacts", "raw.types.InputMessagesFilterDocument", "raw.types.InputMessagesFilterEmpty", "raw.types.InputMessagesFilterGeo", "raw.types.InputMessagesFilterGif", "raw.types.InputMessagesFilterMusic", "raw.types.InputMessagesFilterMyMentions", "raw.types.InputMessagesFilterPhoneCalls", "raw.types.InputMessagesFilterPhotoVideo", "raw.types.InputMessagesFilterPhotos", "raw.types.InputMessagesFilterPinned", "raw.types.InputMessagesFilterRoundVideo", "raw.types.InputMessagesFilterRoundVoice", "raw.types.InputMessagesFilterUrl", "raw.types.InputMessagesFilterVideo", "raw.types.InputMessagesFilterVoice"]


# noinspection PyRedeclaration
class MessagesFilter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessagesFilter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
