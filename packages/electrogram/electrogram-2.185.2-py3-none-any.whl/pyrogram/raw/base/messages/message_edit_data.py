from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageEditData = Union["raw.types.messages.MessageEditData"]


# noinspection PyRedeclaration
class MessageEditData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.MessageEditData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
