from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerSettings = Union["raw.types.PeerSettings"]


# noinspection PyRedeclaration
class PeerSettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PeerSettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
