from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class CheckGiftCode(TLObject):  # type: ignore
    __slots__: List[str] = ["slug"]

    ID = 0x8e51b4c1
    QUALNAME = "functions.payments.CheckGiftCode"

    def __init__(self, *, slug: str) -> None:
        self.slug = slug  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckGiftCode":
        # No flags
        
        slug = String.read(b)
        
        return CheckGiftCode(slug=slug)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.slug))
        
        return b.getvalue()
