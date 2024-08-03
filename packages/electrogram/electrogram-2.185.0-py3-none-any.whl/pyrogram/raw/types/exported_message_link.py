from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ExportedMessageLink(TLObject):  # type: ignore
    __slots__: List[str] = ["link", "html"]

    ID = 0x5dab1af4
    QUALNAME = "types.ExportedMessageLink"

    def __init__(self, *, link: str, html: str) -> None:
        self.link = link  # string
        self.html = html  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportedMessageLink":
        # No flags
        
        link = String.read(b)
        
        html = String.read(b)
        
        return ExportedMessageLink(link=link, html=html)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.link))
        
        b.write(String(self.html))
        
        return b.getvalue()
