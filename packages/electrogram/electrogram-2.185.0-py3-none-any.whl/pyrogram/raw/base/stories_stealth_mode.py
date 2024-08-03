from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StoriesStealthMode = Union["raw.types.StoriesStealthMode"]


# noinspection PyRedeclaration
class StoriesStealthMode:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StoriesStealthMode"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
