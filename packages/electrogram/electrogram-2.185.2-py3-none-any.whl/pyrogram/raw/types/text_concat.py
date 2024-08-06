from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class TextConcat(TLObject):  # type: ignore
    __slots__: List[str] = ["texts"]

    ID = 0x7e6260d7
    QUALNAME = "types.TextConcat"

    def __init__(self, *, texts: List["raw.base.RichText"]) -> None:
        self.texts = texts  # Vector<RichText>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TextConcat":
        # No flags
        
        texts = TLObject.read(b)
        
        return TextConcat(texts=texts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.texts))
        
        return b.getvalue()
