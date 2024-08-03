from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetStarsRevenueStats(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "dark"]

    ID = 0xd91ffad6
    QUALNAME = "functions.payments.GetStarsRevenueStats"

    def __init__(self, *, peer: "raw.base.InputPeer", dark: Optional[bool] = None) -> None:
        self.peer = peer  # InputPeer
        self.dark = dark  # flags.0?true

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStarsRevenueStats":
        
        flags = Int.read(b)
        
        dark = True if flags & (1 << 0) else False
        peer = TLObject.read(b)
        
        return GetStarsRevenueStats(peer=peer, dark=dark)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.dark else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        return b.getvalue()
