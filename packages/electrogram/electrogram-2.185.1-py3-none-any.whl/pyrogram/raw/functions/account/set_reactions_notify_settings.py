from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SetReactionsNotifySettings(TLObject):  # type: ignore
    __slots__: List[str] = ["settings"]

    ID = 0x316ce548
    QUALNAME = "functions.account.SetReactionsNotifySettings"

    def __init__(self, *, settings: "raw.base.ReactionsNotifySettings") -> None:
        self.settings = settings  # ReactionsNotifySettings

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SetReactionsNotifySettings":
        # No flags
        
        settings = TLObject.read(b)
        
        return SetReactionsNotifySettings(settings=settings)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.settings.write())
        
        return b.getvalue()
