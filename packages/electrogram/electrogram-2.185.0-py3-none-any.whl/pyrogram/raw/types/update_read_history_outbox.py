from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UpdateReadHistoryOutbox(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "max_id", "pts", "pts_count"]

    ID = 0x2f2f21bf
    QUALNAME = "types.UpdateReadHistoryOutbox"

    def __init__(self, *, peer: "raw.base.Peer", max_id: int, pts: int, pts_count: int) -> None:
        self.peer = peer  # Peer
        self.max_id = max_id  # int
        self.pts = pts  # int
        self.pts_count = pts_count  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateReadHistoryOutbox":
        # No flags
        
        peer = TLObject.read(b)
        
        max_id = Int.read(b)
        
        pts = Int.read(b)
        
        pts_count = Int.read(b)
        
        return UpdateReadHistoryOutbox(peer=peer, max_id=max_id, pts=pts, pts_count=pts_count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.max_id))
        
        b.write(Int(self.pts))
        
        b.write(Int(self.pts_count))
        
        return b.getvalue()
