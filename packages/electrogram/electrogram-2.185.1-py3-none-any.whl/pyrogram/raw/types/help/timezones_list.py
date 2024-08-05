from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class TimezonesList(TLObject):  # type: ignore
    __slots__: List[str] = ["timezones", "hash"]

    ID = 0x7b74ed71
    QUALNAME = "types.help.TimezonesList"

    def __init__(self, *, timezones: List["raw.base.Timezone"], hash: int) -> None:
        self.timezones = timezones  # Vector<Timezone>
        self.hash = hash  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "TimezonesList":
        # No flags
        
        timezones = TLObject.read(b)
        
        hash = Int.read(b)
        
        return TimezonesList(timezones=timezones, hash=hash)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.timezones))
        
        b.write(Int(self.hash))
        
        return b.getvalue()
