from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ReportSponsoredMessage(TLObject):  # type: ignore
    __slots__: List[str] = ["channel", "random_id", "option"]

    ID = 0xaf8ff6b9
    QUALNAME = "functions.channels.ReportSponsoredMessage"

    def __init__(self, *, channel: "raw.base.InputChannel", random_id: bytes, option: bytes) -> None:
        self.channel = channel  # InputChannel
        self.random_id = random_id  # bytes
        self.option = option  # bytes

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ReportSponsoredMessage":
        # No flags
        
        channel = TLObject.read(b)
        
        random_id = Bytes.read(b)
        
        option = Bytes.read(b)
        
        return ReportSponsoredMessage(channel=channel, random_id=random_id, option=option)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Bytes(self.random_id))
        
        b.write(Bytes(self.option))
        
        return b.getvalue()
