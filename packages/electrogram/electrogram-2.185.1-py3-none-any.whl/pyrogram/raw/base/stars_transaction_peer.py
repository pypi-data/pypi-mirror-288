from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

StarsTransactionPeer = Union["raw.types.StarsTransactionPeer", "raw.types.StarsTransactionPeerAds", "raw.types.StarsTransactionPeerAppStore", "raw.types.StarsTransactionPeerFragment", "raw.types.StarsTransactionPeerPlayMarket", "raw.types.StarsTransactionPeerPremiumBot", "raw.types.StarsTransactionPeerUnsupported"]


# noinspection PyRedeclaration
class StarsTransactionPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.StarsTransactionPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
