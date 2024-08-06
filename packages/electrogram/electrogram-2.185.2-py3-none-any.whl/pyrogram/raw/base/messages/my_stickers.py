from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MyStickers = Union["raw.types.messages.MyStickers"]


# noinspection PyRedeclaration
class MyStickers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.MyStickers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
