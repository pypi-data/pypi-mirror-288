from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CheckedGiftCode = Union["raw.types.payments.CheckedGiftCode"]


# noinspection PyRedeclaration
class CheckedGiftCode:  # type: ignore
    QUALNAME = "pyrogram.raw.base.payments.CheckedGiftCode"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
