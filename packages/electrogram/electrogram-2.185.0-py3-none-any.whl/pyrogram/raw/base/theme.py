from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Theme = Union["raw.types.Theme"]


# noinspection PyRedeclaration
class Theme:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Theme"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
