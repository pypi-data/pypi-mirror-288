from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetBroadcastRevenueTransactions(TLObject):  # type: ignore
    __slots__: List[str] = ["channel", "offset", "limit"]

    ID = 0x69280f
    QUALNAME = "functions.stats.GetBroadcastRevenueTransactions"

    def __init__(self, *, channel: "raw.base.InputChannel", offset: int, limit: int) -> None:
        self.channel = channel  # InputChannel
        self.offset = offset  # int
        self.limit = limit  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBroadcastRevenueTransactions":
        # No flags
        
        channel = TLObject.read(b)
        
        offset = Int.read(b)
        
        limit = Int.read(b)
        
        return GetBroadcastRevenueTransactions(channel=channel, offset=offset, limit=limit)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.offset))
        
        b.write(Int(self.limit))
        
        return b.getvalue()
