from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChannelAdminLogEventActionParticipantJoin(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0x183040d3
    QUALNAME = "types.ChannelAdminLogEventActionParticipantJoin"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionParticipantJoin":
        # No flags
        
        return ChannelAdminLogEventActionParticipantJoin()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
