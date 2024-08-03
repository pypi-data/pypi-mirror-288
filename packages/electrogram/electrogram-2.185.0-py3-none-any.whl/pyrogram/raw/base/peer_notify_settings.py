from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerNotifySettings = Union["raw.types.PeerNotifySettings"]


# noinspection PyRedeclaration
class PeerNotifySettings:  # type: ignore
    QUALNAME = "pyrogram.raw.base.PeerNotifySettings"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
