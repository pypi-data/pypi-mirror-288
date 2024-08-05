from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetBankCardData(TLObject):  # type: ignore
    __slots__: List[str] = ["number"]

    ID = 0x2e79d779
    QUALNAME = "functions.payments.GetBankCardData"

    def __init__(self, *, number: str) -> None:
        self.number = number  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetBankCardData":
        # No flags
        
        number = String.read(b)
        
        return GetBankCardData(number=number)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.number))
        
        return b.getvalue()
