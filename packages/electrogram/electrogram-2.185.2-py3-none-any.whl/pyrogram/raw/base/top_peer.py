from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TopPeer = Union["raw.types.TopPeer"]


# noinspection PyRedeclaration
class TopPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.TopPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
