from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ReceivedNotifyMessage(TLObject):  # type: ignore
    __slots__: List[str] = ["id", "flags"]

    ID = 0xa384b779
    QUALNAME = "types.ReceivedNotifyMessage"

    def __init__(self, *, id: int, flags: int) -> None:
        self.id = id  # int
        self.flags = flags  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReceivedNotifyMessage":
        # No flags
        
        id = Int.read(b)
        
        flags = Int.read(b)
        
        return ReceivedNotifyMessage(id=id, flags=flags)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.id))
        
        b.write(Int(self.flags))
        
        return b.getvalue()
