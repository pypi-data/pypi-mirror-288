from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryReaction = Union["raw.types.StoryReaction", "raw.types.StoryReactionPublicForward", "raw.types.StoryReactionPublicRepost"]


# noinspection PyRedeclaration
class StoryReaction:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StoryReaction"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
