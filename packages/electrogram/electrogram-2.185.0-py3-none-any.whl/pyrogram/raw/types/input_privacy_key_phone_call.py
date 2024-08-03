from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InputPrivacyKeyPhoneCall(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0xfabadc5f
    QUALNAME = "types.InputPrivacyKeyPhoneCall"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPrivacyKeyPhoneCall":
        # No flags
        
        return InputPrivacyKeyPhoneCall()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
