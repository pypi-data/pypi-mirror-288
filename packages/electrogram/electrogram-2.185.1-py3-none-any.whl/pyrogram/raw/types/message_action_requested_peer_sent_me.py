from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageActionRequestedPeerSentMe(TLObject):  # type: ignore
    __slots__: List[str] = ["button_id", "peers"]

    ID = 0x93b31848
    QUALNAME = "types.MessageActionRequestedPeerSentMe"

    def __init__(self, *, button_id: int, peers: List["raw.base.RequestedPeer"]) -> None:
        self.button_id = button_id  # int
        self.peers = peers  # Vector<RequestedPeer>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionRequestedPeerSentMe":
        # No flags
        
        button_id = Int.read(b)
        
        peers = TLObject.read(b)
        
        return MessageActionRequestedPeerSentMe(button_id=button_id, peers=peers)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.button_id))
        
        b.write(Vector(self.peers))
        
        return b.getvalue()
