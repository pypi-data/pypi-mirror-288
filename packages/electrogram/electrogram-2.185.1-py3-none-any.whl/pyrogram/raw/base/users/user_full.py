from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

UserFull = Union["raw.types.users.UserFull"]


# noinspection PyRedeclaration
class UserFull:  # type: ignore
    QUALNAME = "pyrogram.raw.base.users.UserFull"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
