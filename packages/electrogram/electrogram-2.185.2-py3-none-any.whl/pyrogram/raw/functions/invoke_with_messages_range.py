from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InvokeWithMessagesRange(TLObject):  # type: ignore
    __slots__: List[str] = ["range", "query"]

    ID = 0x365275f2
    QUALNAME = "functions.InvokeWithMessagesRange"

    def __init__(self, *, range: "raw.base.MessageRange", query: TLObject) -> None:
        self.range = range  # MessageRange
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InvokeWithMessagesRange":
        # No flags
        
        range = TLObject.read(b)
        
        query = TLObject.read(b)
        
        return InvokeWithMessagesRange(range=range, query=query)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.range.write())
        
        b.write(self.query.write())
        
        return b.getvalue()
