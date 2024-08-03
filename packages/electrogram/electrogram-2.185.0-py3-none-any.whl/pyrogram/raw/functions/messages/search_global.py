from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SearchGlobal(TLObject):  # type: ignore
    __slots__: List[str] = ["q", "filter", "min_date", "max_date", "offset_rate", "offset_peer", "offset_id", "limit", "broadcasts_only", "folder_id"]

    ID = 0x4bc6589a
    QUALNAME = "functions.messages.SearchGlobal"

    def __init__(self, *, q: str, filter: "raw.base.MessagesFilter", min_date: int, max_date: int, offset_rate: int, offset_peer: "raw.base.InputPeer", offset_id: int, limit: int, broadcasts_only: Optional[bool] = None, folder_id: Optional[int] = None) -> None:
        self.q = q  # string
        self.filter = filter  # MessagesFilter
        self.min_date = min_date  # int
        self.max_date = max_date  # int
        self.offset_rate = offset_rate  # int
        self.offset_peer = offset_peer  # InputPeer
        self.offset_id = offset_id  # int
        self.limit = limit  # int
        self.broadcasts_only = broadcasts_only  # flags.1?true
        self.folder_id = folder_id  # flags.0?int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchGlobal":
        
        flags = Int.read(b)
        
        broadcasts_only = True if flags & (1 << 1) else False
        folder_id = Int.read(b) if flags & (1 << 0) else None
        q = String.read(b)
        
        filter = TLObject.read(b)
        
        min_date = Int.read(b)
        
        max_date = Int.read(b)
        
        offset_rate = Int.read(b)
        
        offset_peer = TLObject.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return SearchGlobal(q=q, filter=filter, min_date=min_date, max_date=max_date, offset_rate=offset_rate, offset_peer=offset_peer, offset_id=offset_id, limit=limit, broadcasts_only=broadcasts_only, folder_id=folder_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 1) if self.broadcasts_only else 0
        flags |= (1 << 0) if self.folder_id is not None else 0
        b.write(Int(flags))
        
        if self.folder_id is not None:
            b.write(Int(self.folder_id))
        
        b.write(String(self.q))
        
        b.write(self.filter.write())
        
        b.write(Int(self.min_date))
        
        b.write(Int(self.max_date))
        
        b.write(Int(self.offset_rate))
        
        b.write(self.offset_peer.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
