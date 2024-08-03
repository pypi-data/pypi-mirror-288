from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UpdateStory(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "story"]

    ID = 0x75b3b798
    QUALNAME = "types.UpdateStory"

    def __init__(self, *, peer: "raw.base.Peer", story: "raw.base.StoryItem") -> None:
        self.peer = peer  # Peer
        self.story = story  # StoryItem

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateStory":
        # No flags
        
        peer = TLObject.read(b)
        
        story = TLObject.read(b)
        
        return UpdateStory(peer=peer, story=story)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(self.story.write())
        
        return b.getvalue()
