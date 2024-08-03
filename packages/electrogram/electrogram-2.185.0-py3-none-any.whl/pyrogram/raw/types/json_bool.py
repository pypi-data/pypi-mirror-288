from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class JsonBool(TLObject):  # type: ignore
    __slots__: List[str] = ["value"]

    ID = 0xc7345e6a
    QUALNAME = "types.JsonBool"

    def __init__(self, *, value: bool) -> None:
        self.value = value  # Bool

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "JsonBool":
        # No flags
        
        value = Bool.read(b)
        
        return JsonBool(value=value)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Bool(self.value))
        
        return b.getvalue()
