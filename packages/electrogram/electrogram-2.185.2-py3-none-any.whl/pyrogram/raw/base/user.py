from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

User = Union["raw.types.User", "raw.types.UserEmpty"]


# noinspection PyRedeclaration
class User:  # type: ignore
    QUALNAME = "pyrogram.raw.base.User"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
