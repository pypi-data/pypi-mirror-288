from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CountryCode = Union["raw.types.help.CountryCode"]


# noinspection PyRedeclaration
class CountryCode:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.CountryCode"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
