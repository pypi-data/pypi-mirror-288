from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatFull = Union["raw.types.messages.ChatFull"]


# noinspection PyRedeclaration
class ChatFull:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.ChatFull"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
