from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class BroadcastRevenueBalances(TLObject):  # type: ignore
    __slots__: List[str] = ["current_balance", "available_balance", "overall_revenue"]

    ID = 0x8438f1c6
    QUALNAME = "types.BroadcastRevenueBalances"

    def __init__(self, *, current_balance: int, available_balance: int, overall_revenue: int) -> None:
        self.current_balance = current_balance  # long
        self.available_balance = available_balance  # long
        self.overall_revenue = overall_revenue  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BroadcastRevenueBalances":
        # No flags
        
        current_balance = Long.read(b)
        
        available_balance = Long.read(b)
        
        overall_revenue = Long.read(b)
        
        return BroadcastRevenueBalances(current_balance=current_balance, available_balance=available_balance, overall_revenue=overall_revenue)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.current_balance))
        
        b.write(Long(self.available_balance))
        
        b.write(Long(self.overall_revenue))
        
        return b.getvalue()
