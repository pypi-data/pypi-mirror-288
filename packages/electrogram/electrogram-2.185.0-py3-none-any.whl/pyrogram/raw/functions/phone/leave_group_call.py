from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class LeaveGroupCall(TLObject):  # type: ignore
    __slots__: List[str] = ["call", "source"]

    ID = 0x500377f9
    QUALNAME = "functions.phone.LeaveGroupCall"

    def __init__(self, *, call: "raw.base.InputGroupCall", source: int) -> None:
        self.call = call  # InputGroupCall
        self.source = source  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "LeaveGroupCall":
        # No flags
        
        call = TLObject.read(b)
        
        source = Int.read(b)
        
        return LeaveGroupCall(call=call, source=source)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.call.write())
        
        b.write(Int(self.source))
        
        return b.getvalue()
