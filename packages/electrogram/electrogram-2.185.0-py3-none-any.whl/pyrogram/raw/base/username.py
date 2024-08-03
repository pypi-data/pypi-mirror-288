from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Username = Union["raw.types.Username"]


# noinspection PyRedeclaration
class Username:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Username"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
