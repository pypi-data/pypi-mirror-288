from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ToggleJoinToSend(TLObject):  # type: ignore
    __slots__: List[str] = ["channel", "enabled"]

    ID = 0xe4cb9580
    QUALNAME = "functions.channels.ToggleJoinToSend"

    def __init__(self, *, channel: "raw.base.InputChannel", enabled: bool) -> None:
        self.channel = channel  # InputChannel
        self.enabled = enabled  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ToggleJoinToSend":
        # No flags
        
        channel = TLObject.read(b)
        
        enabled = Bool.read(b)
        
        return ToggleJoinToSend(channel=channel, enabled=enabled)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        b.write(Bool(self.enabled))
        
        return b.getvalue()
