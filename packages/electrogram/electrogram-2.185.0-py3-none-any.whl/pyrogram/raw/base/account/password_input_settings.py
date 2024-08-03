from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PasswordInputSettings = Union["raw.types.account.PasswordInputSettings"]


# noinspection PyRedeclaration
class PasswordInputSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.PasswordInputSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
