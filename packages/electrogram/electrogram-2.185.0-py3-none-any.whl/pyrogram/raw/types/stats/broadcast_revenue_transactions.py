from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class BroadcastRevenueTransactions(TLObject):  # type: ignore
    __slots__: List[str] = ["count", "transactions"]

    ID = 0x87158466
    QUALNAME = "types.stats.BroadcastRevenueTransactions"

    def __init__(self, *, count: int, transactions: List["raw.base.BroadcastRevenueTransaction"]) -> None:
        self.count = count  # int
        self.transactions = transactions  # Vector<BroadcastRevenueTransaction>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BroadcastRevenueTransactions":
        # No flags
        
        count = Int.read(b)
        
        transactions = TLObject.read(b)
        
        return BroadcastRevenueTransactions(count=count, transactions=transactions)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.transactions))
        
        return b.getvalue()
