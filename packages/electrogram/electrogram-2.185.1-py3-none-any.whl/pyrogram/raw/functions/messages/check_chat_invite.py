from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class CheckChatInvite(TLObject):  # type: ignore
    __slots__: List[str] = ["hash"]

    ID = 0x3eadb1bb
    QUALNAME = "functions.messages.CheckChatInvite"

    def __init__(self, *, hash: str) -> None:
        self.hash = hash  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckChatInvite":
        # No flags
        
        hash = String.read(b)
        
        return CheckChatInvite(hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.hash))
        
        return b.getvalue()
