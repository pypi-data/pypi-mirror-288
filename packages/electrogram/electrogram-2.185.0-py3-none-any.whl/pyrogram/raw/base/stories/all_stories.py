from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AllStories = Union["raw.types.stories.AllStories", "raw.types.stories.AllStoriesNotModified"]


# noinspection PyRedeclaration
class AllStories:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stories.AllStories"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
