from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedRingtone = Union["raw.types.account.SavedRingtone", "raw.types.account.SavedRingtoneConverted"]


# noinspection PyRedeclaration
class SavedRingtone:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.SavedRingtone"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
