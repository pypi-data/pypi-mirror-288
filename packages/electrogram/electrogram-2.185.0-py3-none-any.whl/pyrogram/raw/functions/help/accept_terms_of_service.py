from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class AcceptTermsOfService(TLObject):  # type: ignore
    __slots__: List[str] = ["id"]

    ID = 0xee72f79a
    QUALNAME = "functions.help.AcceptTermsOfService"

    def __init__(self, *, id: "raw.base.DataJSON") -> None:
        self.id = id  # DataJSON

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "AcceptTermsOfService":
        # No flags
        
        id = TLObject.read(b)
        
        return AcceptTermsOfService(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.id.write())
        
        return b.getvalue()
