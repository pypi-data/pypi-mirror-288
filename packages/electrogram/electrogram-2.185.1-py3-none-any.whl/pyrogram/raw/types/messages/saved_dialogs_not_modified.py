from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SavedDialogsNotModified(TLObject):  # type: ignore
    __slots__: List[str] = ["count"]

    ID = 0xc01f6fe8
    QUALNAME = "types.messages.SavedDialogsNotModified"

    def __init__(self, *, count: int) -> None:
        self.count = count  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SavedDialogsNotModified":
        # No flags
        
        count = Int.read(b)
        
        return SavedDialogsNotModified(count=count)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        return b.getvalue()
