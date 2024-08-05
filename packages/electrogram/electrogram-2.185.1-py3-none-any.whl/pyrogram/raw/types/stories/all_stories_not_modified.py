from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class AllStoriesNotModified(TLObject):  # type: ignore
    __slots__: List[str] = ["state", "stealth_mode"]

    ID = 0x1158fe3e
    QUALNAME = "types.stories.AllStoriesNotModified"

    def __init__(self, *, state: str, stealth_mode: "raw.base.StoriesStealthMode") -> None:
        self.state = state  # string
        self.stealth_mode = stealth_mode  # StoriesStealthMode

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AllStoriesNotModified":
        
        flags = Int.read(b)
        
        state = String.read(b)
        
        stealth_mode = TLObject.read(b)
        
        return AllStoriesNotModified(state=state, stealth_mode=stealth_mode)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        
        b.write(Int(flags))
        
        b.write(String(self.state))
        
        b.write(self.stealth_mode.write())
        
        return b.getvalue()
