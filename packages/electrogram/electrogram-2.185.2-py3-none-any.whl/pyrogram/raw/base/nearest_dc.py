from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

NearestDc = Union["raw.types.NearestDc"]


# noinspection PyRedeclaration
class NearestDc:  # type: ignore
    QUALNAME = "pyrogram.raw.base.NearestDc"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
