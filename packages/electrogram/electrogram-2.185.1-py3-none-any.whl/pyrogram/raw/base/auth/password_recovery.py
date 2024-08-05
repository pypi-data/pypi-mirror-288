from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PasswordRecovery = Union["raw.types.auth.PasswordRecovery"]


# noinspection PyRedeclaration
class PasswordRecovery:  # type: ignore
    QUALNAME = "pyrogram.raw.base.auth.PasswordRecovery"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
