from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StickerPack = Union["raw.types.StickerPack"]


# noinspection PyRedeclaration
class StickerPack:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StickerPack"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
