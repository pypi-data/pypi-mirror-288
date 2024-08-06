from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class AcceptLoginToken(TLObject):  # type: ignore
    __slots__: List[str] = ["token"]

    ID = 0xe894ad4d
    QUALNAME = "functions.auth.AcceptLoginToken"

    def __init__(self, *, token: bytes) -> None:
        self.token = token  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AcceptLoginToken":
        # No flags
        
        token = Bytes.read(b)
        
        return AcceptLoginToken(token=token)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bytes(self.token))
        
        return b.getvalue()
