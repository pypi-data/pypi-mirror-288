from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BroadcastStats = Union["raw.types.stats.BroadcastStats"]


# noinspection PyRedeclaration
class BroadcastStats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.BroadcastStats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
