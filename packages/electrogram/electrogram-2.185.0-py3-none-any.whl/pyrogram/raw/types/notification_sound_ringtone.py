from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class NotificationSoundRingtone(TLObject):  # type: ignore
    __slots__: List[str] = ["id"]

    ID = 0xff6c8049
    QUALNAME = "types.NotificationSoundRingtone"

    def __init__(self, *, id: int) -> None:
        self.id = id  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "NotificationSoundRingtone":
        # No flags
        
        id = Long.read(b)
        
        return NotificationSoundRingtone(id=id)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.id))
        
        return b.getvalue()
