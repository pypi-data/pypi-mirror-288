from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class TogglePinned(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "id", "pinned"]

    ID = 0x9a75a1ef
    QUALNAME = "functions.stories.TogglePinned"

    def __init__(self, *, peer: "raw.base.InputPeer", id: List[int], pinned: bool) -> None:
        self.peer = peer  # InputPeer
        self.id = id  # Vector<int>
        self.pinned = pinned  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TogglePinned":
        # No flags
        
        peer = TLObject.read(b)
        
        id = TLObject.read(b, Int)
        
        pinned = Bool.read(b)
        
        return TogglePinned(peer=peer, id=id, pinned=pinned)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Vector(self.id, Int))
        
        b.write(Bool(self.pinned))
        
        return b.getvalue()
