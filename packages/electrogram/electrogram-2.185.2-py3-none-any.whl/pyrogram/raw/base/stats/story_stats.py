from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryStats = Union["raw.types.stats.StoryStats"]


# noinspection PyRedeclaration
class StoryStats:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stats.StoryStats"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
