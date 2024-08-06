from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SuggestShortName(TLObject):  # type: ignore
    __slots__: List[str] = ["title"]

    ID = 0x4dafc503
    QUALNAME = "functions.stickers.SuggestShortName"

    def __init__(self, *, title: str) -> None:
        self.title = title  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SuggestShortName":
        # No flags
        
        title = String.read(b)
        
        return SuggestShortName(title=title)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.title))
        
        return b.getvalue()
