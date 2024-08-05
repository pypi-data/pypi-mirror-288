from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class MessageActionSuggestProfilePhoto(TLObject):  # type: ignore
    __slots__: List[str] = ["photo"]

    ID = 0x57de635e
    QUALNAME = "types.MessageActionSuggestProfilePhoto"

    def __init__(self, *, photo: "raw.base.Photo") -> None:
        self.photo = photo  # Photo

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionSuggestProfilePhoto":
        # No flags
        
        photo = TLObject.read(b)
        
        return MessageActionSuggestProfilePhoto(photo=photo)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.photo.write())
        
        return b.getvalue()
