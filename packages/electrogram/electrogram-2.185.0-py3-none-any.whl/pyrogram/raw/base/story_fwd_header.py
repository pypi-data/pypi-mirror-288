from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoryFwdHeader = Union["raw.types.StoryFwdHeader"]


# noinspection PyRedeclaration
class StoryFwdHeader:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StoryFwdHeader"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
