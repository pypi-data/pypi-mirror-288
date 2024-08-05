from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class StatsAbsValueAndPrev(TLObject):  # type: ignore
    __slots__: List[str] = ["current", "previous"]

    ID = 0xcb43acde
    QUALNAME = "types.StatsAbsValueAndPrev"

    def __init__(self, *, current: float, previous: float) -> None:
        self.current = current  # double
        self.previous = previous  # double

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StatsAbsValueAndPrev":
        # No flags
        
        current = Double.read(b)
        
        previous = Double.read(b)
        
        return StatsAbsValueAndPrev(current=current, previous=previous)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Double(self.current))
        
        b.write(Double(self.previous))
        
        return b.getvalue()
