from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputGeoPoint = Union["raw.types.InputGeoPoint", "raw.types.InputGeoPointEmpty"]


# noinspection PyRedeclaration
class InputGeoPoint:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputGeoPoint"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
