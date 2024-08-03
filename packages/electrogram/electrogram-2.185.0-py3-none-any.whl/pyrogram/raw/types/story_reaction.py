from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class StoryReaction(TLObject):  # type: ignore
    __slots__: List[str] = ["peer_id", "date", "reaction"]

    ID = 0x6090d6d5
    QUALNAME = "types.StoryReaction"

    def __init__(self, *, peer_id: "raw.base.Peer", date: int, reaction: "raw.base.Reaction") -> None:
        self.peer_id = peer_id  # Peer
        self.date = date  # int
        self.reaction = reaction  # Reaction

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryReaction":
        # No flags
        
        peer_id = TLObject.read(b)
        
        date = Int.read(b)
        
        reaction = TLObject.read(b)
        
        return StoryReaction(peer_id=peer_id, date=date, reaction=reaction)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer_id.write())
        
        b.write(Int(self.date))
        
        b.write(self.reaction.write())
        
        return b.getvalue()
