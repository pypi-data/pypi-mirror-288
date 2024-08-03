from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PeerColors(TLObject):  # type: ignore
    __slots__: List[str] = ["hash", "colors"]

    ID = 0xf8ed08
    QUALNAME = "types.help.PeerColors"

    def __init__(self, *, hash: int, colors: List["raw.base.help.PeerColorOption"]) -> None:
        self.hash = hash  # int
        self.colors = colors  # Vector<help.PeerColorOption>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PeerColors":
        # No flags
        
        hash = Int.read(b)
        
        colors = TLObject.read(b)
        
        return PeerColors(hash=hash, colors=colors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        b.write(Vector(self.colors))
        
        return b.getvalue()
