from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ChatOnlines = Union["raw.types.ChatOnlines"]


# noinspection PyRedeclaration
class ChatOnlines:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ChatOnlines"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
