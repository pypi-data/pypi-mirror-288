from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ExportedInvoice(TLObject):  # type: ignore
    __slots__: List[str] = ["url"]

    ID = 0xaed0cbd9
    QUALNAME = "types.payments.ExportedInvoice"

    def __init__(self, *, url: str) -> None:
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedInvoice":
        # No flags
        
        url = String.read(b)
        
        return ExportedInvoice(url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        return b.getvalue()
