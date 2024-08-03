from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TopPeerCategoryPeers = Union["raw.types.TopPeerCategoryPeers"]


# noinspection PyRedeclaration
class TopPeerCategoryPeers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.TopPeerCategoryPeers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
