from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StickerSet = Union["raw.types.StickerSet"]


# noinspection PyRedeclaration
class StickerSet:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StickerSet"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
