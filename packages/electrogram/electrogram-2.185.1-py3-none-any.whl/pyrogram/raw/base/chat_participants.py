from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatParticipants = Union["raw.types.ChatParticipants", "raw.types.ChatParticipantsForbidden"]


# noinspection PyRedeclaration
class ChatParticipants:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatParticipants"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
