from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class UserStatusOnline(TLObject):  # type: ignore
    __slots__: List[str] = ["expires"]

    ID = 0xedb93949
    QUALNAME = "types.UserStatusOnline"

    def __init__(self, *, expires: int) -> None:
        self.expires = expires  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "UserStatusOnline":
        # No flags
        
        expires = Int.read(b)
        
        return UserStatusOnline(expires=expires)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.expires))
        
        return b.getvalue()
