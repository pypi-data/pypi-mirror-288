from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InputStorePaymentStarsTopup(TLObject):  # type: ignore
    __slots__: List[str] = ["stars", "currency", "amount"]

    ID = 0xdddd0f56
    QUALNAME = "types.InputStorePaymentStarsTopup"

    def __init__(self, *, stars: int, currency: str, amount: int) -> None:
        self.stars = stars  # long
        self.currency = currency  # string
        self.amount = amount  # long

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputStorePaymentStarsTopup":
        # No flags
        
        stars = Long.read(b)
        
        currency = String.read(b)
        
        amount = Long.read(b)
        
        return InputStorePaymentStarsTopup(stars=stars, currency=currency, amount=amount)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Long(self.stars))
        
        b.write(String(self.currency))
        
        b.write(Long(self.amount))
        
        return b.getvalue()
