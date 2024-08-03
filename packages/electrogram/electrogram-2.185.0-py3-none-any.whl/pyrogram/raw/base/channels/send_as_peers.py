from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

SendAsPeers = Union["raw.types.channels.SendAsPeers"]


# noinspection PyRedeclaration
class SendAsPeers:  # type: ignore
    QUALNAME = "pyrogram.raw.base.channels.SendAsPeers"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
