from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ExportedStoryLink(TLObject):  # type: ignore
    __slots__: List[str] = ["link"]

    ID = 0x3fc9053b
    QUALNAME = "types.ExportedStoryLink"

    def __init__(self, *, link: str) -> None:
        self.link = link  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedStoryLink":
        # No flags
        
        link = String.read(b)
        
        return ExportedStoryLink(link=link)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.link))
        
        return b.getvalue()
