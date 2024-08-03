from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

WallPaper = Union["raw.types.WallPaper", "raw.types.WallPaperNoFile"]


# noinspection PyRedeclaration
class WallPaper:  # type: ignore
    QUALNAME = "pyrogram.raw.base.WallPaper"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
