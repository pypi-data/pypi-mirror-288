from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FoundStory = Union["raw.types.FoundStory"]


# noinspection PyRedeclaration
class FoundStory:  # type: ignore
    QUALNAME = "pyrogram.raw.base.FoundStory"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
