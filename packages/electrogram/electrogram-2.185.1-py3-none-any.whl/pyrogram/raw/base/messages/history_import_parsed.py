from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

HistoryImportParsed = Union["raw.types.messages.HistoryImportParsed"]


# noinspection PyRedeclaration
class HistoryImportParsed:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.HistoryImportParsed"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
