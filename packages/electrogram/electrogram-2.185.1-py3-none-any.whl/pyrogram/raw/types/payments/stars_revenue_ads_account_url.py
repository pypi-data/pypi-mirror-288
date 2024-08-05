from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class StarsRevenueAdsAccountUrl(TLObject):  # type: ignore
    __slots__: List[str] = ["url"]

    ID = 0x394e7f21
    QUALNAME = "types.payments.StarsRevenueAdsAccountUrl"

    def __init__(self, *, url: str) -> None:
        self.url = url  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "StarsRevenueAdsAccountUrl":
        # No flags
        
        url = String.read(b)
        
        return StarsRevenueAdsAccountUrl(url=url)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(String(self.url))
        
        return b.getvalue()
