from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class LoginTokenMigrateTo(TLObject):  # type: ignore
    __slots__: List[str] = ["dc_id", "token"]

    ID = 0x68e9916
    QUALNAME = "types.auth.LoginTokenMigrateTo"

    def __init__(self, *, dc_id: int, token: bytes) -> None:
        self.dc_id = dc_id  # int
        self.token = token  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "LoginTokenMigrateTo":
        # No flags
        
        dc_id = Int.read(b)
        
        token = Bytes.read(b)
        
        return LoginTokenMigrateTo(dc_id=dc_id, token=token)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.dc_id))
        
        b.write(Bytes(self.token))
        
        return b.getvalue()
