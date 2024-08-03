from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UpdateStarsBalance(TLObject):  # type: ignore
    __slots__: List[str] = ["balance"]

    ID = 0xfb85198
    QUALNAME = "types.UpdateStarsBalance"

    def __init__(self, *, balance: int) -> None:
        self.balance = balance  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UpdateStarsBalance":
        # No flags
        
        balance = Long.read(b)
        
        return UpdateStarsBalance(balance=balance)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.balance))
        
        return b.getvalue()
