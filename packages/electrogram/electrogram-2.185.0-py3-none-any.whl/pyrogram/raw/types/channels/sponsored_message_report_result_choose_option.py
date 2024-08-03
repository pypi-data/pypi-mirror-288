from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SponsoredMessageReportResultChooseOption(TLObject):  # type: ignore
    __slots__: List[str] = ["title", "options"]

    ID = 0x846f9e42
    QUALNAME = "types.channels.SponsoredMessageReportResultChooseOption"

    def __init__(self, *, title: str, options: List["raw.base.SponsoredMessageReportOption"]) -> None:
        self.title = title  # string
        self.options = options  # Vector<SponsoredMessageReportOption>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SponsoredMessageReportResultChooseOption":
        # No flags
        
        title = String.read(b)
        
        options = TLObject.read(b)
        
        return SponsoredMessageReportResultChooseOption(title=title, options=options)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.title))
        
        b.write(Vector(self.options))
        
        return b.getvalue()
