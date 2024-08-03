from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class DialogFilterSuggested(TLObject):  # type: ignore
    __slots__: List[str] = ["filter", "description"]

    ID = 0x77744d4a
    QUALNAME = "types.DialogFilterSuggested"

    def __init__(self, *, filter: "raw.base.DialogFilter", description: str) -> None:
        self.filter = filter  # DialogFilter
        self.description = description  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "DialogFilterSuggested":
        # No flags
        
        filter = TLObject.read(b)
        
        description = String.read(b)
        
        return DialogFilterSuggested(filter=filter, description=description)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.filter.write())
        
        b.write(String(self.description))
        
        return b.getvalue()
