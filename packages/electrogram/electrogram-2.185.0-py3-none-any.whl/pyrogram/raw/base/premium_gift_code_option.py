from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PremiumGiftCodeOption = Union["raw.types.PremiumGiftCodeOption"]


# noinspection PyRedeclaration
class PremiumGiftCodeOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PremiumGiftCodeOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
