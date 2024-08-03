from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AppUpdate = Union["raw.types.help.AppUpdate", "raw.types.help.NoAppUpdate"]


# noinspection PyRedeclaration
class AppUpdate:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.AppUpdate"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
