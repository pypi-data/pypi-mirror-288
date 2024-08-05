from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryItem = Union["raw.types.StoryItem", "raw.types.StoryItemDeleted", "raw.types.StoryItemSkipped"]


# noinspection PyRedeclaration
class StoryItem:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StoryItem"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
