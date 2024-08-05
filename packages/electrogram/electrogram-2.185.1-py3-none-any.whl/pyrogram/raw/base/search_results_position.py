from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SearchResultsPosition = Union["raw.types.SearchResultPosition"]


# noinspection PyRedeclaration
class SearchResultsPosition:  # type: ignore
    QUALNAME = "pyrogram.raw.base.SearchResultsPosition"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
