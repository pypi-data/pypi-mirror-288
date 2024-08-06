from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PublicForwards = Union["raw.types.stats.PublicForwards"]


# noinspection PyRedeclaration
class PublicForwards:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.PublicForwards"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
