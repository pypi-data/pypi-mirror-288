from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ConvertToGigagroup(TLObject):  # type: ignore
    __slots__: List[str] = ["channel"]

    ID = 0xb290c69
    QUALNAME = "functions.channels.ConvertToGigagroup"

    def __init__(self, *, channel: "raw.base.InputChannel") -> None:
        self.channel = channel  # InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ConvertToGigagroup":
        # No flags
        
        channel = TLObject.read(b)
        
        return ConvertToGigagroup(channel=channel)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        return b.getvalue()
