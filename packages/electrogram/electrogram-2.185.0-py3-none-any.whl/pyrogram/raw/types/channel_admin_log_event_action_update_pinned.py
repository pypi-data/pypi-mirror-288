from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ChannelAdminLogEventActionUpdatePinned(TLObject):  # type: ignore
    __slots__: List[str] = ["message"]

    ID = 0xe9e82c18
    QUALNAME = "types.ChannelAdminLogEventActionUpdatePinned"

    def __init__(self, *, message: "raw.base.Message") -> None:
        self.message = message  # Message

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChannelAdminLogEventActionUpdatePinned":
        # No flags
        
        message = TLObject.read(b)
        
        return ChannelAdminLogEventActionUpdatePinned(message=message)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.message.write())
        
        return b.getvalue()
