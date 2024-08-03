from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetDocumentByHash(TLObject):  # type: ignore
    __slots__: List[str] = ["sha256", "size", "mime_type"]

    ID = 0xb1f2061f
    QUALNAME = "functions.messages.GetDocumentByHash"

    def __init__(self, *, sha256: bytes, size: int, mime_type: str) -> None:
        self.sha256 = sha256  # bytes
        self.size = size  # long
        self.mime_type = mime_type  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetDocumentByHash":
        # No flags
        
        sha256 = Bytes.read(b)
        
        size = Long.read(b)
        
        mime_type = String.read(b)
        
        return GetDocumentByHash(sha256=sha256, size=size, mime_type=mime_type)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.sha256))
        
        b.write(Long(self.size))
        
        b.write(String(self.mime_type))
        
        return b.getvalue()
