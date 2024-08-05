from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SearchResultsCalendar = Union["raw.types.messages.SearchResultsCalendar"]


# noinspection PyRedeclaration
class SearchResultsCalendar:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.SearchResultsCalendar"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
