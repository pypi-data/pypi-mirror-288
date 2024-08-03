from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class InputPrivacyKeyPhoneP2P(TLObject):  # type: ignore
    __slots__: List[str] = []

    ID = 0xdb9e70d2
    QUALNAME = "types.InputPrivacyKeyPhoneP2P"

    def __init__(self) -> None:
        pass

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "InputPrivacyKeyPhoneP2P":
        # No flags
        
        return InputPrivacyKeyPhoneP2P()

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        return b.getvalue()
