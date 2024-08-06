from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryReactionsList = Union["raw.types.stories.StoryReactionsList"]


# noinspection PyRedeclaration
class StoryReactionsList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stories.StoryReactionsList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
