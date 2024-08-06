from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class EmojiList(TLObject):  # type: ignore
    __slots__: List[str] = ["hash", "document_id"]

    ID = 0x7a1e11d1
    QUALNAME = "types.EmojiList"

    def __init__(self, *, hash: int, document_id: List[int]) -> None:
        self.hash = hash  # long
        self.document_id = document_id  # Vector<long>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "EmojiList":
        # No flags
        
        hash = Long.read(b)
        
        document_id = TLObject.read(b, Long)
        
        return EmojiList(hash=hash, document_id=document_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        b.write(Vector(self.document_id, Long))
        
        return b.getvalue()
