from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PQInnerData = Union["raw.types.PQInnerData", "raw.types.PQInnerDataDc", "raw.types.PQInnerDataTemp", "raw.types.PQInnerDataTempDc"]


# noinspection PyRedeclaration
class PQInnerData:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PQInnerData"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
