from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerStories = Union["raw.types.stories.PeerStories"]


# noinspection PyRedeclaration
class PeerStories:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stories.PeerStories"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
