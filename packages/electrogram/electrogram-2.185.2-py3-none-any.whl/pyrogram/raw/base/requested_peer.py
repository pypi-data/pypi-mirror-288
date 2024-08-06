from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RequestedPeer = Union["raw.types.RequestedPeerChannel", "raw.types.RequestedPeerChat", "raw.types.RequestedPeerUser"]


# noinspection PyRedeclaration
class RequestedPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RequestedPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
