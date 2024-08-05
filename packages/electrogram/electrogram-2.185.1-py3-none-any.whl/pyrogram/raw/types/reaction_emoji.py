from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ReactionEmoji(TLObject):  # type: ignore
    __slots__: List[str] = ["emoticon"]

    ID = 0x1b2286b8
    QUALNAME = "types.ReactionEmoji"

    def __init__(self, *, emoticon: str) -> None:
        self.emoticon = emoticon  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReactionEmoji":
        # No flags
        
        emoticon = String.read(b)
        
        return ReactionEmoji(emoticon=emoticon)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.emoticon))
        
        return b.getvalue()
