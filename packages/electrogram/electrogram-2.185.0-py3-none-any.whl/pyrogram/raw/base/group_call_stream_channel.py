from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupCallStreamChannel = Union["raw.types.GroupCallStreamChannel"]


# noinspection PyRedeclaration
class GroupCallStreamChannel:  # type: ignore
    QUALNAME = "pyrogram.raw.base.GroupCallStreamChannel"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
