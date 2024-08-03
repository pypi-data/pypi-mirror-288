from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

UserStatus = Union["raw.types.UserStatusEmpty", "raw.types.UserStatusLastMonth", "raw.types.UserStatusLastWeek", "raw.types.UserStatusOffline", "raw.types.UserStatusOnline", "raw.types.UserStatusRecently"]


# noinspection PyRedeclaration
class UserStatus:  # type: ignore
    QUALNAME = "pyrogram.raw.base.UserStatus"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
