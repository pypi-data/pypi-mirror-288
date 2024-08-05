from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SetDefaultHistoryTTL(TLObject):  # type: ignore
    __slots__: List[str] = ["period"]

    ID = 0x9eb51445
    QUALNAME = "functions.messages.SetDefaultHistoryTTL"

    def __init__(self, *, period: int) -> None:
        self.period = period  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetDefaultHistoryTTL":
        # No flags
        
        period = Int.read(b)
        
        return SetDefaultHistoryTTL(period=period)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.period))
        
        return b.getvalue()
