from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetNotifySettings(TLObject):  # type: ignore
    __slots__: List[str] = ["peer"]

    ID = 0x12b3ad31
    QUALNAME = "functions.account.GetNotifySettings"

    def __init__(self, *, peer: "raw.base.InputNotifyPeer") -> None:
        self.peer = peer  # InputNotifyPeer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetNotifySettings":
        # No flags
        
        peer = TLObject.read(b)
        
        return GetNotifySettings(peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
