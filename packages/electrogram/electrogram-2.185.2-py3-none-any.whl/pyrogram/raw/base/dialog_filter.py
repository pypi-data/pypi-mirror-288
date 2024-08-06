from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DialogFilter = Union["raw.types.DialogFilter", "raw.types.DialogFilterChatlist", "raw.types.DialogFilterDefault"]


# noinspection PyRedeclaration
class DialogFilter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DialogFilter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
