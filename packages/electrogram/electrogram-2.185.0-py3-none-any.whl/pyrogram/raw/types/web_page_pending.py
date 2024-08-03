from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class WebPagePending(TLObject):  # type: ignore
    __slots__: List[str] = ["id", "date", "url"]

    ID = 0xb0d13e47
    QUALNAME = "types.WebPagePending"

    def __init__(self, *, id: int, date: int, url: Optional[str] = None) -> None:
        self.id = id  # long
        self.date = date  # int
        self.url = url  # flags.0?string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "WebPagePending":
        
        flags = Int.read(b)
        
        id = Long.read(b)
        
        url = String.read(b) if flags & (1 << 0) else None
        date = Int.read(b)
        
        return WebPagePending(id=id, date=date, url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        flags |= (1 << 0) if self.url is not None else 0
        b.write(Int(flags))
        
        b.write(Long(self.id))
        
        if self.url is not None:
            b.write(String(self.url))
        
        b.write(Int(self.date))
        
        return b.getvalue()
