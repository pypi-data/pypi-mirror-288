from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerDialogs = Union["raw.types.messages.PeerDialogs"]


# noinspection PyRedeclaration
class PeerDialogs:  # type: ignore
    QUALNAME = "pyrogram.raw.base.messages.PeerDialogs"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
