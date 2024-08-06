from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PromoData = Union["raw.types.help.PromoData", "raw.types.help.PromoDataEmpty"]


# noinspection PyRedeclaration
class PromoData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.PromoData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
