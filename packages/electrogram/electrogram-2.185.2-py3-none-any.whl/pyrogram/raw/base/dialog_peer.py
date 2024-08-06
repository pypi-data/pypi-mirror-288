from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

DialogPeer = Union["raw.types.DialogPeer", "raw.types.DialogPeerFolder"]


# noinspection PyRedeclaration
class DialogPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.DialogPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
