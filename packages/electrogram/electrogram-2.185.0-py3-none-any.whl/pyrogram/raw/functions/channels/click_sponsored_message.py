from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ClickSponsoredMessage(TLObject):  # type: ignore
    __slots__: List[str] = ["channel", "random_id"]

    ID = 0x18afbc93
    QUALNAME = "functions.channels.ClickSponsoredMessage"

    def __init__(self, *, channel: "raw.base.InputChannel", random_id: bytes) -> None:
        self.channel = channel  # InputChannel
        self.random_id = random_id  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ClickSponsoredMessage":
        # No flags
        
        channel = TLObject.read(b)
        
        random_id = Bytes.read(b)
        
        return ClickSponsoredMessage(channel=channel, random_id=random_id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Bytes(self.random_id))
        
        return b.getvalue()
