from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsPercentValue = Union["raw.types.StatsPercentValue"]


# noinspection PyRedeclaration
class StatsPercentValue:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsPercentValue"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
