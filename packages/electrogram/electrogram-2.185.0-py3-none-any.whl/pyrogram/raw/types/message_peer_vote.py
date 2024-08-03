from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessagePeerVote(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "option", "date"]

    ID = 0xb6cc2d5c
    QUALNAME = "types.MessagePeerVote"

    def __init__(self, *, peer: "raw.base.Peer", option: bytes, date: int) -> None:
        self.peer = peer  # Peer
        self.option = option  # bytes
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessagePeerVote":
        # No flags
        
        peer = TLObject.read(b)
        
        option = Bytes.read(b)
        
        date = Int.read(b)
        
        return MessagePeerVote(peer=peer, option=option, date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        b.write(Bytes(self.option))
        
        b.write(Int(self.date))
        
        return b.getvalue()
