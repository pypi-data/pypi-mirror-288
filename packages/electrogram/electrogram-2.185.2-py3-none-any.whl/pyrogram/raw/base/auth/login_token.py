from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

LoginToken = Union["raw.types.auth.LoginToken", "raw.types.auth.LoginTokenMigrateTo", "raw.types.auth.LoginTokenSuccess"]


# noinspection PyRedeclaration
class LoginToken:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.LoginToken"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
