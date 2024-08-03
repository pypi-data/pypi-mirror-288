from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class CdnPublicKey(TLObject):  # type: ignore
    __slots__: List[str] = ["dc_id", "public_key"]

    ID = 0xc982eaba
    QUALNAME = "types.CdnPublicKey"

    def __init__(self, *, dc_id: int, public_key: str) -> None:
        self.dc_id = dc_id  # int
        self.public_key = public_key  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "CdnPublicKey":
        # No flags
        
        dc_id = Int.read(b)
        
        public_key = String.read(b)
        
        return CdnPublicKey(dc_id=dc_id, public_key=public_key)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.dc_id))
        
        b.write(String(self.public_key))
        
        return b.getvalue()
