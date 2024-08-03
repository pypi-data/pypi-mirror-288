from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetIsPremiumRequiredToContact(TLObject):  # type: ignore
    __slots__: List[str] = ["id"]

    ID = 0xa622aa10
    QUALNAME = "functions.users.GetIsPremiumRequiredToContact"

    def __init__(self, *, id: List["raw.base.InputUser"]) -> None:
        self.id = id  # Vector<InputUser>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetIsPremiumRequiredToContact":
        # No flags
        
        id = TLObject.read(b)
        
        return GetIsPremiumRequiredToContact(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.id))
        
        return b.getvalue()
