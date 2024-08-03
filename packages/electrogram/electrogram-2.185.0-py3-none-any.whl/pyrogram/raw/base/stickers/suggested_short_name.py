from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SuggestedShortName = Union["raw.types.stickers.SuggestedShortName"]


# noinspection PyRedeclaration
class SuggestedShortName:  # type: ignore
    QUALNAME = "pyrogram.raw.base.stickers.SuggestedShortName"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
