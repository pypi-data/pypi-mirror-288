from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryViews = Union["raw.types.StoryViews"]


# noinspection PyRedeclaration
class StoryViews:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StoryViews"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
