from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SearchCounter = Union["raw.types.messages.SearchCounter"]


# noinspection PyRedeclaration
class SearchCounter:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SearchCounter"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
