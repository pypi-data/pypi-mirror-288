from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class GetLeaveChatlistSuggestions(TLObject):  # type: ignore
    __slots__: List[str] = ["chatlist"]

    ID = 0xfdbcd714
    QUALNAME = "functions.chatlists.GetLeaveChatlistSuggestions"

    def __init__(self, *, chatlist: "raw.base.InputChatlist") -> None:
        self.chatlist = chatlist  # InputChatlist

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "GetLeaveChatlistSuggestions":
        # No flags
        
        chatlist = TLObject.read(b)
        
        return GetLeaveChatlistSuggestions(chatlist=chatlist)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.chatlist.write())
        
        return b.getvalue()
