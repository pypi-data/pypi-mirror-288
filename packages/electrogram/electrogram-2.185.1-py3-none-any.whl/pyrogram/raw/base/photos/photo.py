from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Photo = Union["raw.types.photos.Photo"]


# noinspection PyRedeclaration
class Photo:  # type: ignore
    QUALNAME = "pyrogram.raw.base.photos.Photo"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
