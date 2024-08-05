from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

LoggedOut = Union["raw.types.auth.LoggedOut"]


# noinspection PyRedeclaration
class LoggedOut:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.LoggedOut"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
