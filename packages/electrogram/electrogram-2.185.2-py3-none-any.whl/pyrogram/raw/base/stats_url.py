from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsURL = Union["raw.types.StatsURL"]


# noinspection PyRedeclaration
class StatsURL:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsURL"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
