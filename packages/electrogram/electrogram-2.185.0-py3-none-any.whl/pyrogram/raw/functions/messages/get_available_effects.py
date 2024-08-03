from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetAvailableEffects(TLObject):  # type: ignore
    __slots__: List[str] = ["hash"]

    ID = 0xdea20a39
    QUALNAME = "functions.messages.GetAvailableEffects"

    def __init__(self, *, hash: int) -> None:
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetAvailableEffects":
        # No flags
        
        hash = Int.read(b)
        
        return GetAvailableEffects(hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.hash))
        
        return b.getvalue()
