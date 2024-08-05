from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

CheckedHistoryImportPeer = Union["raw.types.messages.CheckedHistoryImportPeer"]


# noinspection PyRedeclaration
class CheckedHistoryImportPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.CheckedHistoryImportPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
