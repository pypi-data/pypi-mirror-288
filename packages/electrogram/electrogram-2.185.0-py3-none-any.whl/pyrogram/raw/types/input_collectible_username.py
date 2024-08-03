from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InputCollectibleUsername(TLObject):  # type: ignore
    __slots__: List[str] = ["username"]

    ID = 0xe39460a9
    QUALNAME = "types.InputCollectibleUsername"

    def __init__(self, *, username: str) -> None:
        self.username = username  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputCollectibleUsername":
        # No flags
        
        username = String.read(b)
        
        return InputCollectibleUsername(username=username)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.username))
        
        return b.getvalue()
