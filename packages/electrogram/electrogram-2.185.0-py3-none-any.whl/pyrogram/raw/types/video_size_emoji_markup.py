from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class VideoSizeEmojiMarkup(TLObject):  # type: ignore
    __slots__: List[str] = ["emoji_id", "background_colors"]

    ID = 0xf85c413c
    QUALNAME = "types.VideoSizeEmojiMarkup"

    def __init__(self, *, emoji_id: int, background_colors: List[int]) -> None:
        self.emoji_id = emoji_id  # long
        self.background_colors = background_colors  # Vector<int>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "VideoSizeEmojiMarkup":
        # No flags
        
        emoji_id = Long.read(b)
        
        background_colors = TLObject.read(b, Int)
        
        return VideoSizeEmojiMarkup(emoji_id=emoji_id, background_colors=background_colors)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.emoji_id))
        
        b.write(Vector(self.background_colors, Int))
        
        return b.getvalue()
