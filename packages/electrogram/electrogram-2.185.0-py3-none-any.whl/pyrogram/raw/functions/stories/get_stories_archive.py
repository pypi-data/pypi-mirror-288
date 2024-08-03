from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetStoriesArchive(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "offset_id", "limit"]

    ID = 0xb4352016
    QUALNAME = "functions.stories.GetStoriesArchive"

    def __init__(self, *, peer: "raw.base.InputPeer", offset_id: int, limit: int) -> None:
        self.peer = peer  # InputPeer
        self.offset_id = offset_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetStoriesArchive":
        # No flags
        
        peer = TLObject.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return GetStoriesArchive(peer=peer, offset_id=offset_id, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
