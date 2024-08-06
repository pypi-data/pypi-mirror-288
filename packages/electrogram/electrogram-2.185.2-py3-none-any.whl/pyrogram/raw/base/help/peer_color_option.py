from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

PeerColorOption = Union["raw.types.help.PeerColorOption"]


# noinspection PyRedeclaration
class PeerColorOption:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.PeerColorOption"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
