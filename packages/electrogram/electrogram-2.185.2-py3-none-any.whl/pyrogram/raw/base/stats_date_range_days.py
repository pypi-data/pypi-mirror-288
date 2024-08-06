from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsDateRangeDays = Union["raw.types.StatsDateRangeDays"]


# noinspection PyRedeclaration
class StatsDateRangeDays:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsDateRangeDays"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
