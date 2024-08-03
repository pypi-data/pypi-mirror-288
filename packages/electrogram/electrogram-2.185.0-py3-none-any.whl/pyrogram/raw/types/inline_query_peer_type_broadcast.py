from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InlineQueryPeerTypeBroadcast(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0x6334ee9a
    QUALNAME = "types.InlineQueryPeerTypeBroadcast"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InlineQueryPeerTypeBroadcast":
        # No flags
        
        return InlineQueryPeerTypeBroadcast()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
