from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DeactivateAllUsernames(TLObject):  # type: ignore
    __slots__: List[str] = ["channel"]

    ID = 0xa245dd3
    QUALNAME = "functions.channels.DeactivateAllUsernames"

    def __init__(self, *, channel: "raw.base.InputChannel") -> None:
        self.channel = channel  # InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DeactivateAllUsernames":
        # No flags
        
        channel = TLObject.read(b)
        
        return DeactivateAllUsernames(channel=channel)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.channel.write())
        
        return b.getvalue()
