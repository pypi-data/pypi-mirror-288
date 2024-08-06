from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DataJSON(TLObject):  # type: ignore
    __slots__: List[str] = ["data"]

    ID = 0x7d748d04
    QUALNAME = "types.DataJSON"

    def __init__(self, *, data: str) -> None:
        self.data = data  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DataJSON":
        # No flags
        
        data = String.read(b)
        
        return DataJSON(data=data)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.data))
        
        return b.getvalue()
