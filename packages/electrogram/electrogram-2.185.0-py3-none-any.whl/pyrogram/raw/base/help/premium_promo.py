from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PremiumPromo = Union["raw.types.help.PremiumPromo"]


# noinspection PyRedeclaration
class PremiumPromo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.PremiumPromo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
