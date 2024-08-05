from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmailVerified = Union["raw.types.account.EmailVerified", "raw.types.account.EmailVerifiedLogin"]


# noinspection PyRedeclaration
class EmailVerified:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.EmailVerified"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
