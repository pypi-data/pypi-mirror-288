from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InvokeWithLayer(TLObject):  # type: ignore
    __slots__: List[str] = ["layer", "query"]

    ID = 0xda9b0d0d
    QUALNAME = "functions.InvokeWithLayer"

    def __init__(self, *, layer: int, query: TLObject) -> None:
        self.layer = layer  # int
        self.query = query  # !X

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InvokeWithLayer":
        # No flags
        
        layer = Int.read(b)
        
        query = TLObject.read(b)
        
        return InvokeWithLayer(layer=layer, query=query)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.layer))
        
        b.write(self.query.write())
        
        return b.getvalue()
