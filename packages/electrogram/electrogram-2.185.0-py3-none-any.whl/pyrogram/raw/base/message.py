from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Message = Union["raw.types.Message", "raw.types.MessageEmpty", "raw.types.MessageService"]


# noinspection PyRedeclaration
class Message:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Message"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
