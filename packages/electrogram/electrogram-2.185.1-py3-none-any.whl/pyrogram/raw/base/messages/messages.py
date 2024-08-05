from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Messages = Union["raw.types.messages.ChannelMessages", "raw.types.messages.Messages", "raw.types.messages.MessagesNotModified", "raw.types.messages.MessagesSlice"]


# noinspection PyRedeclaration
class Messages:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.Messages"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
