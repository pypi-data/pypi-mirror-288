from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WallPaperSettings = Union["raw.types.WallPaperSettings"]


# noinspection PyRedeclaration
class WallPaperSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WallPaperSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
