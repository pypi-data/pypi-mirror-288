from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsGroupTopPoster = Union["raw.types.StatsGroupTopPoster"]


# noinspection PyRedeclaration
class StatsGroupTopPoster:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsGroupTopPoster"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
