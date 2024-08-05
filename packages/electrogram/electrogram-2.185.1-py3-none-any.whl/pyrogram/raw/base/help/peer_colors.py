from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerColors = Union["raw.types.help.PeerColors", "raw.types.help.PeerColorsNotModified"]


# noinspection PyRedeclaration
class PeerColors:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.PeerColors"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
