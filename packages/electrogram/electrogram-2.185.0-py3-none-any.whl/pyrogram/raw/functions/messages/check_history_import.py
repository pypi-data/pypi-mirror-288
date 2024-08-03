from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class CheckHistoryImport(TLObject):  # type: ignore
    __slots__: List[str] = ["import_head"]

    ID = 0x43fe19f3
    QUALNAME = "functions.messages.CheckHistoryImport"

    def __init__(self, *, import_head: str) -> None:
        self.import_head = import_head  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckHistoryImport":
        # No flags
        
        import_head = String.read(b)
        
        return CheckHistoryImport(import_head=import_head)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.import_head))
        
        return b.getvalue()
