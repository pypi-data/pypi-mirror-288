from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessWeeklyOpen = Union["raw.types.BusinessWeeklyOpen"]


# noinspection PyRedeclaration
class BusinessWeeklyOpen:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessWeeklyOpen"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
