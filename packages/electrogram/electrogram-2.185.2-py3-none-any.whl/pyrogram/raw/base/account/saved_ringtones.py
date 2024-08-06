from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SavedRingtones = Union["raw.types.account.SavedRingtones", "raw.types.account.SavedRingtonesNotModified"]


# noinspection PyRedeclaration
class SavedRingtones:  # type: ignore
    QUALNAME = "pyrogram.raw.base.account.SavedRingtones"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
