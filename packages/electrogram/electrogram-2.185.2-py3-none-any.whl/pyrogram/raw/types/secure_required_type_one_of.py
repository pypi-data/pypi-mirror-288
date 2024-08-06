from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SecureRequiredTypeOneOf(TLObject):  # type: ignore
    __slots__: List[str] = ["types"]

    ID = 0x27477b4
    QUALNAME = "types.SecureRequiredTypeOneOf"

    def __init__(self, *, types: List["raw.base.SecureRequiredType"]) -> None:
        self.types = types  # Vector<SecureRequiredType>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SecureRequiredTypeOneOf":
        # No flags
        
        types = TLObject.read(b)
        
        return SecureRequiredTypeOneOf(types=types)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.types))
        
        return b.getvalue()
