from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChannelParticipantsKicked(TLObject):  # type: ignore
    __slots__: List[str] = ["q"]

    ID = 0xa3b54985
    QUALNAME = "types.ChannelParticipantsKicked"

    def __init__(self, *, q: str) -> None:
        self.q = q  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelParticipantsKicked":
        # No flags
        
        q = String.read(b)
        
        return ChannelParticipantsKicked(q=q)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.q))
        
        return b.getvalue()
