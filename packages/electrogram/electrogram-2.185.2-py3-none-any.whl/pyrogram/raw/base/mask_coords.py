from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

MaskCoords = Union["raw.types.MaskCoords"]


# noinspection PyRedeclaration
class MaskCoords:  # type: ignore
    QUALNAME = "pyrogram.raw.base.MaskCoords"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
