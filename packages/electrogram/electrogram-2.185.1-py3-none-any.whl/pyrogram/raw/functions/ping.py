from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class Ping(TLObject):  # type: ignore
    __slots__: List[str] = ["ping_id"]

    ID = 0x7abe77ec
    QUALNAME = "functions.Ping"

    def __init__(self, *, ping_id: int) -> None:
        self.ping_id = ping_id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Ping":
        # No flags
        
        ping_id = Long.read(b)
        
        return Ping(ping_id=ping_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.ping_id))
        
        return b.getvalue()
