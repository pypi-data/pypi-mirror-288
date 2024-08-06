from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DraftMessage = Union["raw.types.DraftMessage", "raw.types.DraftMessageEmpty"]


# noinspection PyRedeclaration
class DraftMessage:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DraftMessage"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
