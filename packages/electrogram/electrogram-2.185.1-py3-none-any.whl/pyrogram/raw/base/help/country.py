from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Country = Union["raw.types.help.Country"]


# noinspection PyRedeclaration
class Country:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.Country"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
