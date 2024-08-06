from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GroupCallStreamChannels(TLObject):  # type: ignore
    __slots__: List[str] = ["channels"]

    ID = 0xd0e482b2
    QUALNAME = "types.phone.GroupCallStreamChannels"

    def __init__(self, *, channels: List["raw.base.GroupCallStreamChannel"]) -> None:
        self.channels = channels  # Vector<GroupCallStreamChannel>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GroupCallStreamChannels":
        # No flags
        
        channels = TLObject.read(b)
        
        return GroupCallStreamChannels(channels=channels)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.channels))
        
        return b.getvalue()
