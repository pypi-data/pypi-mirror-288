from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PasswordSettings = Union["raw.types.account.PasswordSettings"]


# noinspection PyRedeclaration
class PasswordSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.PasswordSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
