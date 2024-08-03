from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ToggleSlowMode(TLObject):  # type: ignore
    __slots__: List[str] = ["channel", "seconds"]

    ID = 0xedd49ef0
    QUALNAME = "functions.channels.ToggleSlowMode"

    def __init__(self, *, channel: "raw.base.InputChannel", seconds: int) -> None:
        self.channel = channel  # InputChannel
        self.seconds = seconds  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleSlowMode":
        # No flags
        
        channel = TLObject.read(b)
        
        seconds = Int.read(b)
        
        return ToggleSlowMode(channel=channel, seconds=seconds)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Int(self.seconds))
        
        return b.getvalue()
