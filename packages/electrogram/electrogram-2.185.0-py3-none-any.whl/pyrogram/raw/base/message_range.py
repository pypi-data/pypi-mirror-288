from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageRange = Union["raw.types.MessageRange"]


# noinspection PyRedeclaration
class MessageRange:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MessageRange"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
