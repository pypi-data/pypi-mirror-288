from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SecureValueErrorFiles(TLObject):  # type: ignore
    __slots__: List[str] = ["type", "file_hash", "text"]

    ID = 0x666220e9
    QUALNAME = "types.SecureValueErrorFiles"

    def __init__(self, *, type: "raw.base.SecureValueType", file_hash: List[bytes], text: str) -> None:
        self.type = type  # SecureValueType
        self.file_hash = file_hash  # Vector<bytes>
        self.text = text  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SecureValueErrorFiles":
        # No flags
        
        type = TLObject.read(b)
        
        file_hash = TLObject.read(b, Bytes)
        
        text = String.read(b)
        
        return SecureValueErrorFiles(type=type, file_hash=file_hash, text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.type.write())
        
        b.write(Vector(self.file_hash, Bytes))
        
        b.write(String(self.text))
        
        return b.getvalue()
