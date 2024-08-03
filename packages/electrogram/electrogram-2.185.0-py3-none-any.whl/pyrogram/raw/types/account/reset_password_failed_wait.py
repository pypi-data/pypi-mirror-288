from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ResetPasswordFailedWait(TLObject):  # type: ignore
    __slots__: List[str] = ["retry_date"]

    ID = 0xe3779861
    QUALNAME = "types.account.ResetPasswordFailedWait"

    def __init__(self, *, retry_date: int) -> None:
        self.retry_date = retry_date  # int

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ResetPasswordFailedWait":
        # No flags
        
        retry_date = Int.read(b)
        
        return ResetPasswordFailedWait(retry_date=retry_date)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.retry_date))
        
        return b.getvalue()
