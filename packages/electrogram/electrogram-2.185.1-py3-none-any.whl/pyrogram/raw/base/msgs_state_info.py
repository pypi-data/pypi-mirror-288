from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MsgsStateInfo = Union["raw.types.MsgsStateInfo"]


# noinspection PyRedeclaration
class MsgsStateInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MsgsStateInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
