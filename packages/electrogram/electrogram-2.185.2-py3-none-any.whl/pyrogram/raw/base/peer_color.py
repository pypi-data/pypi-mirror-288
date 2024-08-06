from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerColor = Union["raw.types.PeerColor"]


# noinspection PyRedeclaration
class PeerColor:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PeerColor"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
