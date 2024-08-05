from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupCallStreamRtmpUrl = Union["raw.types.phone.GroupCallStreamRtmpUrl"]


# noinspection PyRedeclaration
class GroupCallStreamRtmpUrl:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.GroupCallStreamRtmpUrl"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
