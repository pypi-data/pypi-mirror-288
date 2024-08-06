from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageMediaPaidMedia(TLObject):  # type: ignore
    __slots__: List[str] = ["stars_amount", "extended_media"]

    ID = 0xa8852491
    QUALNAME = "types.MessageMediaPaidMedia"

    def __init__(self, *, stars_amount: int, extended_media: List["raw.base.MessageExtendedMedia"]) -> None:
        self.stars_amount = stars_amount  # long
        self.extended_media = extended_media  # Vector<MessageExtendedMedia>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageMediaPaidMedia":
        # No flags
        
        stars_amount = Long.read(b)
        
        extended_media = TLObject.read(b)
        
        return MessageMediaPaidMedia(stars_amount=stars_amount, extended_media=extended_media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.stars_amount))
        
        b.write(Vector(self.extended_media))
        
        return b.getvalue()
