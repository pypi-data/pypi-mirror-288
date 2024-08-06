from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetContactSignUpNotification(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0x9f07c728
    QUALNAME = "functions.account.GetContactSignUpNotification"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetContactSignUpNotification":
        # No flags
        
        return GetContactSignUpNotification()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
