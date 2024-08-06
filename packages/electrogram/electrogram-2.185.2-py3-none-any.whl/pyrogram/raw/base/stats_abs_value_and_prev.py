from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsAbsValueAndPrev = Union["raw.types.StatsAbsValueAndPrev"]


# noinspection PyRedeclaration
class StatsAbsValueAndPrev:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsAbsValueAndPrev"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
