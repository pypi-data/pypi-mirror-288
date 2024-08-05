from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DocumentAttributeImageSize(TLObject):  # type: ignore
    __slots__: List[str] = ["w", "h"]

    ID = 0x6c37c15c
    QUALNAME = "types.DocumentAttributeImageSize"

    def __init__(self, *, w: int, h: int) -> None:
        self.w = w  # int
        self.h = h  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DocumentAttributeImageSize":
        # No flags
        
        w = Int.read(b)
        
        h = Int.read(b)
        
        return DocumentAttributeImageSize(w=w, h=h)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.w))
        
        b.write(Int(self.h))
        
        return b.getvalue()
