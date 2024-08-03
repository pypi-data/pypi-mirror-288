from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetSearchCounters(TLObject):  # type: ignore
    __slots__: List[str] = ["peer", "filters", "saved_peer_id", "top_msg_id"]

    ID = 0x1bbcf300
    QUALNAME = "functions.messages.GetSearchCounters"

    def __init__(self, *, peer: "raw.base.InputPeer", filters: List["raw.base.MessagesFilter"], saved_peer_id: "raw.base.InputPeer" = None, top_msg_id: Optional[int] = None) -> None:
        self.peer = peer  # InputPeer
        self.filters = filters  # Vector<MessagesFilter>
        self.saved_peer_id = saved_peer_id  # flags.2?InputPeer
        self.top_msg_id = top_msg_id  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetSearchCounters":
        
        flags = Int.read(b)
        
        peer = TLObject.read(b)
        
        saved_peer_id = TLObject.read(b) if flags & (1 << 2) else None
        
        top_msg_id = Int.read(b) if flags & (1 << 0) else None
        filters = TLObject.read(b)
        
        return GetSearchCounters(peer=peer, filters=filters, saved_peer_id=saved_peer_id, top_msg_id=top_msg_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 2) if self.saved_peer_id is not None else 0
        flags |= (1 << 0) if self.top_msg_id is not None else 0
        b.write(Int(flags))
        
        b.write(self.peer.write())
        
        if self.saved_peer_id is not None:
            b.write(self.saved_peer_id.write())
        
        if self.top_msg_id is not None:
            b.write(Int(self.top_msg_id))
        
        b.write(Vector(self.filters))
        
        return b.getvalue()
