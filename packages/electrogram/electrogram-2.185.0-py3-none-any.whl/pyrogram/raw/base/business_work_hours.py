from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessWorkHours = Union["raw.types.BusinessWorkHours"]


# noinspection PyRedeclaration
class BusinessWorkHours:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessWorkHours"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
