from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class LoginTokenSuccess(TLObject):  # type: ignore
    __slots__: List[str] = ["authorization"]

    ID = 0x390d5c5e
    QUALNAME = "types.auth.LoginTokenSuccess"

    def __init__(self, *, authorization: "raw.base.auth.Authorization") -> None:
        self.authorization = authorization  # auth.Authorization

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "LoginTokenSuccess":
        # No flags
        
        authorization = TLObject.read(b)
        
        return LoginTokenSuccess(authorization=authorization)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.authorization.write())
        
        return b.getvalue()
