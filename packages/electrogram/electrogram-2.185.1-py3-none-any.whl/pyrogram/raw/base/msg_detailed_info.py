from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MsgDetailedInfo = Union["raw.types.MsgDetailedInfo", "raw.types.MsgNewDetailedInfo"]


# noinspection PyRedeclaration
class MsgDetailedInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MsgDetailedInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
