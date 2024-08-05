from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

QuickReply = Union["raw.types.QuickReply"]


# noinspection PyRedeclaration
class QuickReply:  # type: ignore
    QUALNAME = "pyrogram.raw.base.QuickReply"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
