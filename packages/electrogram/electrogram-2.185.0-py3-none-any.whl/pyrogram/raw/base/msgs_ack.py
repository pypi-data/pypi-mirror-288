from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MsgsAck = Union["raw.types.MsgsAck"]


# noinspection PyRedeclaration
class MsgsAck:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MsgsAck"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
