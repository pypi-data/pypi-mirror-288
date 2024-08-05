from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

AttachMenuPeerType = Union["raw.types.AttachMenuPeerTypeBotPM", "raw.types.AttachMenuPeerTypeBroadcast", "raw.types.AttachMenuPeerTypeChat", "raw.types.AttachMenuPeerTypePM", "raw.types.AttachMenuPeerTypeSameBotPM"]


# noinspection PyRedeclaration
class AttachMenuPeerType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.AttachMenuPeerType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
