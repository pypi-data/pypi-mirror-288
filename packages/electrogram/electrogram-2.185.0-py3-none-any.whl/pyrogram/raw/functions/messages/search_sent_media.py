from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SearchSentMedia(TLObject):  # type: ignore
    __slots__: List[str] = ["q", "filter", "limit"]

    ID = 0x107e31a0
    QUALNAME = "functions.messages.SearchSentMedia"

    def __init__(self, *, q: str, filter: "raw.base.MessagesFilter", limit: int) -> None:
        self.q = q  # string
        self.filter = filter  # MessagesFilter
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchSentMedia":
        # No flags
        
        q = String.read(b)
        
        filter = TLObject.read(b)
        
        limit = Int.read(b)
        
        return SearchSentMedia(q=q, filter=filter, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        b.write(self.filter.write())
        
        b.write(Int(self.limit))
        
        return b.getvalue()
