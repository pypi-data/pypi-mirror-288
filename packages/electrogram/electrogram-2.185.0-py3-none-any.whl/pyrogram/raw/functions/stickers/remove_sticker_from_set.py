from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class RemoveStickerFromSet(TLObject):  # type: ignore
    __slots__: List[str] = ["sticker"]

    ID = 0xf7760f51
    QUALNAME = "functions.stickers.RemoveStickerFromSet"

    def __init__(self, *, sticker: "raw.base.InputDocument") -> None:
        self.sticker = sticker  # InputDocument

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "RemoveStickerFromSet":
        # No flags
        
        sticker = TLObject.read(b)
        
        return RemoveStickerFromSet(sticker=sticker)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.sticker.write())
        
        return b.getvalue()
