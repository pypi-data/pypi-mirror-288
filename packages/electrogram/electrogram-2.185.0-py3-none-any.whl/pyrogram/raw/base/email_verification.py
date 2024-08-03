from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmailVerification = Union["raw.types.EmailVerificationApple", "raw.types.EmailVerificationCode", "raw.types.EmailVerificationGoogle"]


# noinspection PyRedeclaration
class EmailVerification:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmailVerification"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
