from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TopPeers = Union["raw.types.contacts.TopPeers", "raw.types.contacts.TopPeersDisabled", "raw.types.contacts.TopPeersNotModified"]


# noinspection PyRedeclaration
class TopPeers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.contacts.TopPeers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
