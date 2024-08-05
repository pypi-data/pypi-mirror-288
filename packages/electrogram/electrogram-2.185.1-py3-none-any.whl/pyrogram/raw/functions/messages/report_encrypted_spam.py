from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ReportEncryptedSpam(TLObject):  # type: ignore
    __slots__: List[str] = ["peer"]

    ID = 0x4b0c8c0f
    QUALNAME = "functions.messages.ReportEncryptedSpam"

    def __init__(self, *, peer: "raw.base.InputEncryptedChat") -> None:
        self.peer = peer  # InputEncryptedChat

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReportEncryptedSpam":
        # No flags
        
        peer = TLObject.read(b)
        
        return ReportEncryptedSpam(peer=peer)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.peer.write())
        
        return b.getvalue()
