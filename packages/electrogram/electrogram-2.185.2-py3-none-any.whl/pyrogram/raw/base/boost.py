from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Boost = Union["raw.types.Boost"]


# noinspection PyRedeclaration
class Boost:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Boost"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
