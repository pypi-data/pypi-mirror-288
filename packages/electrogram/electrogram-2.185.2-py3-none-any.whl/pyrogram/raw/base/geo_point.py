from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

GeoPoint = Union["raw.types.GeoPoint", "raw.types.GeoPointEmpty"]


# noinspection PyRedeclaration
class GeoPoint:  # type: ignore
    QUALNAME = "pyrogram.raw.base.GeoPoint"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
