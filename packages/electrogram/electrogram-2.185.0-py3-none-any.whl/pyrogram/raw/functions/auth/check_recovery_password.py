from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class CheckRecoveryPassword(TLObject):  # type: ignore
    __slots__: List[str] = ["code"]

    ID = 0xd36bf79
    QUALNAME = "functions.auth.CheckRecoveryPassword"

    def __init__(self, *, code: str) -> None:
        self.code = code  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CheckRecoveryPassword":
        # No flags
        
        code = String.read(b)
        
        return CheckRecoveryPassword(code=code)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.code))
        
        return b.getvalue()
