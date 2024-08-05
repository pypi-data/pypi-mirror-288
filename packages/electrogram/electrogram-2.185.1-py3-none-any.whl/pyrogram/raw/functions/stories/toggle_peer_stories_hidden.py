from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class TogglePeerStoriesHidden(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "hidden"]

    ID = 0xbd0415c4
    QUALNAME = "functions.stories.TogglePeerStoriesHidden"

    def __init__(self, *, peer: "raw.base.InputPeer", hidden: bool) -> None:
        self.peer = peer  # InputPeer
        self.hidden = hidden  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TogglePeerStoriesHidden":
        # No flags
        
        peer = TLObject.read(b)
        
        hidden = Bool.read(b)
        
        return TogglePeerStoriesHidden(peer=peer, hidden=hidden)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bool(self.hidden))
        
        return b.getvalue()
