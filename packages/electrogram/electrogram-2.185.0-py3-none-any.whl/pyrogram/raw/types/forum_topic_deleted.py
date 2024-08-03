from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ForumTopicDeleted(TLObject):  # type: ignore
    __slots__: List[str] = ["id"]

    ID = 0x23f109b
    QUALNAME = "types.ForumTopicDeleted"

    def __init__(self, *, id: int) -> None:
        self.id = id  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ForumTopicDeleted":
        # No flags
        
        id = Int.read(b)
        
        return ForumTopicDeleted(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        return b.getvalue()
