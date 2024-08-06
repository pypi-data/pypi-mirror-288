from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SendStarsForm(TLObject):  # type: ignore
    __slots__: List[str] = ["form_id", "invoice"]

    ID = 0x2bb731d
    QUALNAME = "functions.payments.SendStarsForm"

    def __init__(self, *, form_id: int, invoice: "raw.base.InputInvoice") -> None:
        self.form_id = form_id  # long
        self.invoice = invoice  # InputInvoice

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SendStarsForm":
        
        flags = Int.read(b)
        
        form_id = Long.read(b)
        
        invoice = TLObject.read(b)
        
        return SendStarsForm(form_id=form_id, invoice=invoice)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        flags = 0
        
        b.write(Int(flags))
        
        b.write(Long(self.form_id))
        
        b.write(self.invoice.write())
        
        return b.getvalue()
