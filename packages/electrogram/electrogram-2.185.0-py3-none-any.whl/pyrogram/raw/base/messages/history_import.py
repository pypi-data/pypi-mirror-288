from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

HistoryImport = Union["raw.types.messages.HistoryImport"]


# noinspection PyRedeclaration
class HistoryImport:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.HistoryImport"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
