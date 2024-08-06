from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PhotoSize = Union["raw.types.PhotoCachedSize", "raw.types.PhotoPathSize", "raw.types.PhotoSize", "raw.types.PhotoSizeEmpty", "raw.types.PhotoSizeProgressive", "raw.types.PhotoStrippedSize"]


# noinspection PyRedeclaration
class PhotoSize:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PhotoSize"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
