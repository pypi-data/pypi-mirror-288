from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InviteText(TLObject):  # type: ignore
    __slots__: List[str] = ["message"]

    ID = 0x18cb9f78
    QUALNAME = "types.help.InviteText"

    def __init__(self, *, message: str) -> None:
        self.message = message  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InviteText":
        # No flags
        
        message = String.read(b)
        
        return InviteText(message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.message))
        
        return b.getvalue()
