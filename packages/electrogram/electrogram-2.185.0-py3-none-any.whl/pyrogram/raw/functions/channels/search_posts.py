from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SearchPosts(TLObject):  # type: ignore
    __slots__: List[str] = ["hashtag", "offset_rate", "offset_peer", "offset_id", "limit"]

    ID = 0xd19f987b
    QUALNAME = "functions.channels.SearchPosts"

    def __init__(self, *, hashtag: str, offset_rate: int, offset_peer: "raw.base.InputPeer", offset_id: int, limit: int) -> None:
        self.hashtag = hashtag  # string
        self.offset_rate = offset_rate  # int
        self.offset_peer = offset_peer  # InputPeer
        self.offset_id = offset_id  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchPosts":
        # No flags
        
        hashtag = String.read(b)
        
        offset_rate = Int.read(b)
        
        offset_peer = TLObject.read(b)
        
        offset_id = Int.read(b)
        
        limit = Int.read(b)
        
        return SearchPosts(hashtag=hashtag, offset_rate=offset_rate, offset_peer=offset_peer, offset_id=offset_id, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.hashtag))
        
        b.write(Int(self.offset_rate))
        
        b.write(self.offset_peer.write())
        
        b.write(Int(self.offset_id))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
