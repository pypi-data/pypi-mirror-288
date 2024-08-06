from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SearchResultsPositions = Union["raw.types.messages.SearchResultsPositions"]


# noinspection PyRedeclaration
class SearchResultsPositions:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SearchResultsPositions"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
