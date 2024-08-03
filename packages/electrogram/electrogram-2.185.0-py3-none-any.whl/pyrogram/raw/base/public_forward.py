from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PublicForward = Union["raw.types.PublicForwardMessage", "raw.types.PublicForwardStory"]


# noinspection PyRedeclaration
class PublicForward:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PublicForward"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
