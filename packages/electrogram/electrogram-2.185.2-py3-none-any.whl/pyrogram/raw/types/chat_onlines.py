from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChatOnlines(TLObject):  # type: ignore
    __slots__: List[str] = ["onlines"]

    ID = 0xf041e250
    QUALNAME = "types.ChatOnlines"

    def __init__(self, *, onlines: int) -> None:
        self.onlines = onlines  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatOnlines":
        # No flags
        
        onlines = Int.read(b)
        
        return ChatOnlines(onlines=onlines)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.onlines))
        
        return b.getvalue()
