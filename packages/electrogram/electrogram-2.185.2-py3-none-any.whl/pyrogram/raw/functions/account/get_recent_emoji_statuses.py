from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetRecentEmojiStatuses(TLObject):  # type: ignore
    __slots__: List[str] = ["hash"]

    ID = 0xf578105
    QUALNAME = "functions.account.GetRecentEmojiStatuses"

    def __init__(self, *, hash: int) -> None:
        self.hash = hash  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetRecentEmojiStatuses":
        # No flags
        
        hash = Long.read(b)
        
        return GetRecentEmojiStatuses(hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.hash))
        
        return b.getvalue()
