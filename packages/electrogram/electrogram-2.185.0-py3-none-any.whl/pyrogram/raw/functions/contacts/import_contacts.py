from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class ImportContacts(TLObject):  # type: ignore
    __slots__: List[str] = ["contacts"]

    ID = 0x2c800be5
    QUALNAME = "functions.contacts.ImportContacts"

    def __init__(self, *, contacts: List["raw.base.InputContact"]) -> None:
        self.contacts = contacts  # Vector<InputContact>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ImportContacts":
        # No flags
        
        contacts = TLObject.read(b)
        
        return ImportContacts(contacts=contacts)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.contacts))
        
        return b.getvalue()
