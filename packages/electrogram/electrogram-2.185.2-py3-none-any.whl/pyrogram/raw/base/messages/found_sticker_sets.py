from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

FoundStickerSets = Union["raw.types.messages.FoundStickerSets", "raw.types.messages.FoundStickerSetsNotModified"]


# noinspection PyRedeclaration
class FoundStickerSets:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.FoundStickerSets"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
