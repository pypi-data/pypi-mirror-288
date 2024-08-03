from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Updates = Union["raw.types.UpdateShort", "raw.types.UpdateShortChatMessage", "raw.types.UpdateShortMessage", "raw.types.UpdateShortSentMessage", "raw.types.Updates", "raw.types.UpdatesCombined", "raw.types.UpdatesTooLong"]


# noinspection PyRedeclaration
class Updates:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Updates"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
