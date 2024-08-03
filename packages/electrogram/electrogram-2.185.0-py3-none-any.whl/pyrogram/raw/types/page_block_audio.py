from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PageBlockAudio(TLObject):  # type: ignore
    __slots__: List[str] = ["audio_id", "caption"]

    ID = 0x804361ea
    QUALNAME = "types.PageBlockAudio"

    def __init__(self, *, audio_id: int, caption: "raw.base.PageCaption") -> None:
        self.audio_id = audio_id  # long
        self.caption = caption  # PageCaption

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockAudio":
        # No flags
        
        audio_id = Long.read(b)
        
        caption = TLObject.read(b)
        
        return PageBlockAudio(audio_id=audio_id, caption=caption)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.audio_id))
        
        b.write(self.caption.write())
        
        return b.getvalue()
