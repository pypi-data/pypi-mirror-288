from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

RequestPeerType = Union["raw.types.RequestPeerTypeBroadcast", "raw.types.RequestPeerTypeChat", "raw.types.RequestPeerTypeUser"]


# noinspection PyRedeclaration
class RequestPeerType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.RequestPeerType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
