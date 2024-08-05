from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SupportName = Union["raw.types.help.SupportName"]


# noinspection PyRedeclaration
class SupportName:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.SupportName"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
