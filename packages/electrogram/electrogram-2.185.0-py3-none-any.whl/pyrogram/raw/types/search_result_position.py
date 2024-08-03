from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SearchResultPosition(TLObject):  # type: ignore
    __slots__: List[str] = ["msg_id", "date", "offset"]

    ID = 0x7f648b67
    QUALNAME = "types.SearchResultPosition"

    def __init__(self, *, msg_id: int, date: int, offset: int) -> None:
        self.msg_id = msg_id  # int
        self.date = date  # int
        self.offset = offset  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SearchResultPosition":
        # No flags
        
        msg_id = Int.read(b)
        
        date = Int.read(b)
        
        offset = Int.read(b)
        
        return SearchResultPosition(msg_id=msg_id, date=date, offset=offset)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.msg_id))
        
        b.write(Int(self.date))
        
        b.write(Int(self.offset))
        
        return b.getvalue()
