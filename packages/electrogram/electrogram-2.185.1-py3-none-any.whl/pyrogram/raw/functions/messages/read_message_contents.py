from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ReadMessageContents(TLObject):  # type: ignore
    __slots__: List[str] = ["id"]

    ID = 0x36a73f77
    QUALNAME = "functions.messages.ReadMessageContents"

    def __init__(self, *, id: List[int]) -> None:
        self.id = id  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReadMessageContents":
        # No flags
        
        id = TLObject.read(b, Int)
        
        return ReadMessageContents(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id, Int))
        
        return b.getvalue()
