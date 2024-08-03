from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerLocated = Union["raw.types.PeerLocated", "raw.types.PeerSelfLocated"]


# noinspection PyRedeclaration
class PeerLocated:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PeerLocated"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
