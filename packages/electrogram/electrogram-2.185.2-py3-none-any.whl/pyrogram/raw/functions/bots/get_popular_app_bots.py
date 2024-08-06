from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetPopularAppBots(TLObject):  # type: ignore
    __slots__: List[str] = ["offset", "limit"]

    ID = 0xc2510192
    QUALNAME = "functions.bots.GetPopularAppBots"

    def __init__(self, *, offset: str, limit: int) -> None:
        self.offset = offset  # string
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetPopularAppBots":
        # No flags
        
        offset = String.read(b)
        
        limit = Int.read(b)
        
        return GetPopularAppBots(offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
