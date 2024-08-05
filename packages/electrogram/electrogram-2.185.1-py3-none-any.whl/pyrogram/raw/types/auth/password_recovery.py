from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PasswordRecovery(TLObject):  # type: ignore
    __slots__: List[str] = ["email_pattern"]

    ID = 0x137948a5
    QUALNAME = "types.auth.PasswordRecovery"

    def __init__(self, *, email_pattern: str) -> None:
        self.email_pattern = email_pattern  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PasswordRecovery":
        # No flags
        
        email_pattern = String.read(b)
        
        return PasswordRecovery(email_pattern=email_pattern)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.email_pattern))
        
        return b.getvalue()
