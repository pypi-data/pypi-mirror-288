from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryViewsList = Union["raw.types.stories.StoryViewsList"]


# noinspection PyRedeclaration
class StoryViewsList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stories.StoryViewsList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
