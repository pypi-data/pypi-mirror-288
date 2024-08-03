from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SetDiscussionGroup(TLObject):  # type: ignore
    __slots__: List[str] = ["broadcast", "group"]

    ID = 0x40582bb2
    QUALNAME = "functions.channels.SetDiscussionGroup"

    def __init__(self, *, broadcast: "raw.base.InputChannel", group: "raw.base.InputChannel") -> None:
        self.broadcast = broadcast  # InputChannel
        self.group = group  # InputChannel

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetDiscussionGroup":
        # No flags
        
        broadcast = TLObject.read(b)
        
        group = TLObject.read(b)
        
        return SetDiscussionGroup(broadcast=broadcast, group=group)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.broadcast.write())
        
        b.write(self.group.write())
        
        return b.getvalue()
