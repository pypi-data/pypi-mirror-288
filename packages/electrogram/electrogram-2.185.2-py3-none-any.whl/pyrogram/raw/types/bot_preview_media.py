from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class BotPreviewMedia(TLObject):  # type: ignore
    __slots__: List[str] = ["date", "media"]

    ID = 0x23e91ba3
    QUALNAME = "types.BotPreviewMedia"

    def __init__(self, *, date: int, media: "raw.base.MessageMedia") -> None:
        self.date = date  # int
        self.media = media  # MessageMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "BotPreviewMedia":
        # No flags
        
        date = Int.read(b)
        
        media = TLObject.read(b)
        
        return BotPreviewMedia(date=date, media=media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.date))
        
        b.write(self.media.write())
        
        return b.getvalue()
