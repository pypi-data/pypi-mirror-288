from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class OutboxReadDate(TLObject):  # type: ignore
    __slots__: List[str] = ["date"]

    ID = 0x3bb842ac
    QUALNAME = "types.OutboxReadDate"

    def __init__(self, *, date: int) -> None:
        self.date = date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "OutboxReadDate":
        # No flags
        
        date = Int.read(b)
        
        return OutboxReadDate(date=date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        return b.getvalue()
