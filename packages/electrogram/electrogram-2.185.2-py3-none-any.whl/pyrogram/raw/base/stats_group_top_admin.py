from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsGroupTopAdmin = Union["raw.types.StatsGroupTopAdmin"]


# noinspection PyRedeclaration
class StatsGroupTopAdmin:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsGroupTopAdmin"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
