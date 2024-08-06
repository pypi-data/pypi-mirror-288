from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerColorSet = Union["raw.types.help.PeerColorProfileSet", "raw.types.help.PeerColorSet"]


# noinspection PyRedeclaration
class PeerColorSet:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.PeerColorSet"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
