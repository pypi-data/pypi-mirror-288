from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class Support(TLObject):  # type: ignore
    __slots__: List[str] = ["phone_number", "user"]

    ID = 0x17c6b5f6
    QUALNAME = "types.help.Support"

    def __init__(self, *, phone_number: str, user: "raw.base.User") -> None:
        self.phone_number = phone_number  # string
        self.user = user  # User

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "Support":
        # No flags
        
        phone_number = String.read(b)
        
        user = TLObject.read(b)
        
        return Support(phone_number=phone_number, user=user)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.phone_number))
        
        b.write(self.user.write())
        
        return b.getvalue()
