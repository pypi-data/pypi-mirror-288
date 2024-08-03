from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class JoinGroupCallPresentation(TLObject):  # type: ignore
    __slots__: List[str] = ["call", "params"]

    ID = 0xcbea6bc4
    QUALNAME = "functions.phone.JoinGroupCallPresentation"

    def __init__(self, *, call: "raw.base.InputGroupCall", params: "raw.base.DataJSON") -> None:
        self.call = call  # InputGroupCall
        self.params = params  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JoinGroupCallPresentation":
        # No flags
        
        call = TLObject.read(b)
        
        params = TLObject.read(b)
        
        return JoinGroupCallPresentation(call=call, params=params)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.call.write())
        
        b.write(self.params.write())
        
        return b.getvalue()
