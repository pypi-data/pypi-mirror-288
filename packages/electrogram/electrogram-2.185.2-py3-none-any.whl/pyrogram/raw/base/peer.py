from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Peer = Union["raw.types.PeerChannel", "raw.types.PeerChat", "raw.types.PeerUser"]


# noinspection PyRedeclaration
class Peer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Peer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
