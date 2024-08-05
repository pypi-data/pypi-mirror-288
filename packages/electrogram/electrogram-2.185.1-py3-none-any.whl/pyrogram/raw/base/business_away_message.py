from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

BusinessAwayMessage = Union["raw.types.BusinessAwayMessage"]


# noinspection PyRedeclaration
class BusinessAwayMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.BusinessAwayMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
