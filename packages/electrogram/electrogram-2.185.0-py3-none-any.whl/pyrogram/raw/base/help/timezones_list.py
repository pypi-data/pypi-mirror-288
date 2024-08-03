from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TimezonesList = Union["raw.types.help.TimezonesList", "raw.types.help.TimezonesListNotModified"]


# noinspection PyRedeclaration
class TimezonesList:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.TimezonesList"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
