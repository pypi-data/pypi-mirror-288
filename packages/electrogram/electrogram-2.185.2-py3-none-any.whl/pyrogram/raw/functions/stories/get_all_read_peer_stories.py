from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetAllReadPeerStories(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0x9b5ae7f9
    QUALNAME = "functions.stories.GetAllReadPeerStories"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetAllReadPeerStories":
        # No flags
        
        return GetAllReadPeerStories()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
