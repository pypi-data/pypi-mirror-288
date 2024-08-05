from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChannelParticipantLeft(TLObject):  # type: ignore
    __slots__: List[str] = ["peer"]

    ID = 0x1b03f006
    QUALNAME = "types.ChannelParticipantLeft"

    def __init__(self, *, peer: "raw.base.Peer") -> None:
        self.peer = peer  # Peer

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelParticipantLeft":
        # No flags
        
        peer = TLObject.read(b)
        
        return ChannelParticipantLeft(peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
