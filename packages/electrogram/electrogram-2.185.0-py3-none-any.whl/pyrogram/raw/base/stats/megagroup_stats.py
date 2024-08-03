from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MegagroupStats = Union["raw.types.stats.MegagroupStats"]


# noinspection PyRedeclaration
class MegagroupStats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.MegagroupStats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
