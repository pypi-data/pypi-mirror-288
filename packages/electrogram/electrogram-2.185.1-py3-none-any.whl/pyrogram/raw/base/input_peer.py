from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

InputPeer = Union["raw.types.InputPeerChannel", "raw.types.InputPeerChannelFromMessage", "raw.types.InputPeerChat", "raw.types.InputPeerEmpty", "raw.types.InputPeerSelf", "raw.types.InputPeerUser", "raw.types.InputPeerUserFromMessage"]


# noinspection PyRedeclaration
class InputPeer:  # type: ignore
    QUALNAME = "pyrogram.raw.base.InputPeer"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
