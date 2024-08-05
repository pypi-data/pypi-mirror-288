from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MsgsAllInfo = Union["raw.types.MsgsAllInfo"]


# noinspection PyRedeclaration
class MsgsAllInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MsgsAllInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
