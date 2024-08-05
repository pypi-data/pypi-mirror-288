from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PremiumGiftOption = Union["raw.types.PremiumGiftOption"]


# noinspection PyRedeclaration
class PremiumGiftOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PremiumGiftOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
