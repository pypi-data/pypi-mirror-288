from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

ThemeSettings = Union["raw.types.ThemeSettings"]


# noinspection PyRedeclaration
class ThemeSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.ThemeSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
