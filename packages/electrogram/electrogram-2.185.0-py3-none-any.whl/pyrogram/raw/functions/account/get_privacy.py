from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetPrivacy(TLObject):  # type: ignore
    __slots__: List[str] = ["key"]

    ID = 0xdadbc950
    QUALNAME = "functions.account.GetPrivacy"

    def __init__(self, *, key: "raw.base.InputPrivacyKey") -> None:
        self.key = key  # InputPrivacyKey

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetPrivacy":
        # No flags
        
        key = TLObject.read(b)
        
        return GetPrivacy(key=key)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.key.write())
        
        return b.getvalue()
