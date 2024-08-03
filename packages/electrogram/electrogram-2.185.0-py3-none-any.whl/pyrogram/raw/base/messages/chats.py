from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Chats = Union["raw.types.messages.Chats", "raw.types.messages.ChatsSlice"]


# noinspection PyRedeclaration
class Chats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.Chats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
