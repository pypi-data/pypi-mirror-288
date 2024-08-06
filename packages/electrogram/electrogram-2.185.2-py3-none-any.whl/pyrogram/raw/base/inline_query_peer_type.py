from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InlineQueryPeerType = Union["raw.types.InlineQueryPeerTypeBotPM", "raw.types.InlineQueryPeerTypeBroadcast", "raw.types.InlineQueryPeerTypeChat", "raw.types.InlineQueryPeerTypeMegagroup", "raw.types.InlineQueryPeerTypePM", "raw.types.InlineQueryPeerTypeSameBotPM"]


# noinspection PyRedeclaration
class InlineQueryPeerType:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InlineQueryPeerType"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
