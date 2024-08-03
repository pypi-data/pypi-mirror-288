from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

EmailVerifyPurpose = Union["raw.types.EmailVerifyPurposeLoginChange", "raw.types.EmailVerifyPurposeLoginSetup", "raw.types.EmailVerifyPurposePassport"]


# noinspection PyRedeclaration
class EmailVerifyPurpose:  # type: ignore
    QUALNAME = "pyrogram.raw.base.EmailVerifyPurpose"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
