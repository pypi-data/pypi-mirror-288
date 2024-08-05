from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PageBlockSubtitle(TLObject):  # type: ignore
    __slots__: List[str] = ["text"]

    ID = 0x8ffa9a1f
    QUALNAME = "types.PageBlockSubtitle"

    def __init__(self, *, text: "raw.base.RichText") -> None:
        self.text = text  # RichText

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockSubtitle":
        # No flags
        
        text = TLObject.read(b)
        
        return PageBlockSubtitle(text=text)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.text.write())
        
        return b.getvalue()
