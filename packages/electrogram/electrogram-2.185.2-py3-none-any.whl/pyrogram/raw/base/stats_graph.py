from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsGraph = Union["raw.types.StatsGraph", "raw.types.StatsGraphAsync", "raw.types.StatsGraphError"]


# noinspection PyRedeclaration
class StatsGraph:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsGraph"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
