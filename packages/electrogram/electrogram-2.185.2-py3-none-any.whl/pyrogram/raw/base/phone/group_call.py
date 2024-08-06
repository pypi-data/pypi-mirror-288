from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupCall = Union["raw.types.phone.GroupCall"]


# noinspection PyRedeclaration
class GroupCall:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.GroupCall"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
