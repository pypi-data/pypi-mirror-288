from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SendMessageHistoryImportAction(TLObject):  # type: ignore
    __slots__: List[str] = ["progress"]

    ID = 0xdbda9246
    QUALNAME = "types.SendMessageHistoryImportAction"

    def __init__(self, *, progress: int) -> None:
        self.progress = progress  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendMessageHistoryImportAction":
        # No flags
        
        progress = Int.read(b)
        
        return SendMessageHistoryImportAction(progress=progress)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.progress))
        
        return b.getvalue()
