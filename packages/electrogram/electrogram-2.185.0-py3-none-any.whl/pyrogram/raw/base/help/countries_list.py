from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CountriesList = Union["raw.types.help.CountriesList", "raw.types.help.CountriesListNotModified"]


# noinspection PyRedeclaration
class CountriesList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.CountriesList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
