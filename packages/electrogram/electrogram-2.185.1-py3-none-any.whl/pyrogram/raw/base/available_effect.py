from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AvailableEffect = Union["raw.types.AvailableEffect"]


# noinspection PyRedeclaration
class AvailableEffect:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AvailableEffect"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
