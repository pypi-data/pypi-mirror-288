from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class StoryReactionPublicForward(TLObject):  # type: ignore
    __slots__: List[str] = ["message"]

    ID = 0xbbab2643
    QUALNAME = "types.StoryReactionPublicForward"

    def __init__(self, *, message: "raw.base.Message") -> None:
        self.message = message  # Message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StoryReactionPublicForward":
        # No flags
        
        message = TLObject.read(b)
        
        return StoryReactionPublicForward(message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.message.write())
        
        return b.getvalue()
