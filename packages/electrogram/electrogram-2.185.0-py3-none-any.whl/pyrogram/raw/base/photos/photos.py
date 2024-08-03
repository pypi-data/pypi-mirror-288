from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Photos = Union["raw.types.photos.Photos", "raw.types.photos.PhotosSlice"]


# noinspection PyRedeclaration
class Photos:  # type: ignore
    QUALNAME = "pyrogram.raw.base.photos.Photos"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
