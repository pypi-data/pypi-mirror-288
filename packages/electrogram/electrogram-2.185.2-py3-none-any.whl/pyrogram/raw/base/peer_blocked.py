from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerBlocked = Union["raw.types.PeerBlocked"]


# noinspection PyRedeclaration
class PeerBlocked:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PeerBlocked"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
