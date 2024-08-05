from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MessageStats = Union["raw.types.stats.MessageStats"]


# noinspection PyRedeclaration
class MessageStats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.MessageStats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
