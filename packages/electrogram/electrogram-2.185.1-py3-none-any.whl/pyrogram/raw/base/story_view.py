from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryView = Union["raw.types.StoryView", "raw.types.StoryViewPublicForward", "raw.types.StoryViewPublicRepost"]


# noinspection PyRedeclaration
class StoryView:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StoryView"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
