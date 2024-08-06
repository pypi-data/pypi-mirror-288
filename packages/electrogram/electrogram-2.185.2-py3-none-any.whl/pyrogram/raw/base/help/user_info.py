from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

UserInfo = Union["raw.types.help.UserInfo", "raw.types.help.UserInfoEmpty"]


# noinspection PyRedeclaration
class UserInfo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.UserInfo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
