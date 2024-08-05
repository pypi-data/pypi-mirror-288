from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StatsGroupTopInviter = Union["raw.types.StatsGroupTopInviter"]


# noinspection PyRedeclaration
class StatsGroupTopInviter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StatsGroupTopInviter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
