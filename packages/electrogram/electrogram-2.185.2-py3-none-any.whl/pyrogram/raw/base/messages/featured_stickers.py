from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FeaturedStickers = Union["raw.types.messages.FeaturedStickers", "raw.types.messages.FeaturedStickersNotModified"]


# noinspection PyRedeclaration
class FeaturedStickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.FeaturedStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
