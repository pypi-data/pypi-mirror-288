from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputWallPaper = Union["raw.types.InputWallPaper", "raw.types.InputWallPaperNoFile", "raw.types.InputWallPaperSlug"]


# noinspection PyRedeclaration
class InputWallPaper:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputWallPaper"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
