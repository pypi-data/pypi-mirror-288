from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AvailableEffects = Union["raw.types.messages.AvailableEffects", "raw.types.messages.AvailableEffectsNotModified"]


# noinspection PyRedeclaration
class AvailableEffects:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.AvailableEffects"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
