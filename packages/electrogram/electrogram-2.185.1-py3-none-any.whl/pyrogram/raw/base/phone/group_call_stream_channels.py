from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GroupCallStreamChannels = Union["raw.types.phone.GroupCallStreamChannels"]


# noinspection PyRedeclaration
class GroupCallStreamChannels:  # type: ignore
    QUALNAME = "pyrogram.raw.base.phone.GroupCallStreamChannels"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
