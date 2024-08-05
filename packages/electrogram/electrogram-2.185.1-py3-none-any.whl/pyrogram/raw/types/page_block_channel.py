from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class PageBlockChannel(TLObject):  # type: ignore
    __slots__: List[str] = ["channel"]

    ID = 0xef1751b5
    QUALNAME = "types.PageBlockChannel"

    def __init__(self, *, channel: "raw.base.Chat") -> None:
        self.channel = channel  # Chat

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "PageBlockChannel":
        # No flags
        
        channel = TLObject.read(b)
        
        return PageBlockChannel(channel=channel)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        return b.getvalue()
