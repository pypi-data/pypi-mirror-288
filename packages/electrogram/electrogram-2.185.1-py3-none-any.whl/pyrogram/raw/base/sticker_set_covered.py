from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StickerSetCovered = Union["raw.types.StickerSetCovered", "raw.types.StickerSetFullCovered", "raw.types.StickerSetMultiCovered", "raw.types.StickerSetNoCovered"]


# noinspection PyRedeclaration
class StickerSetCovered:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StickerSetCovered"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
