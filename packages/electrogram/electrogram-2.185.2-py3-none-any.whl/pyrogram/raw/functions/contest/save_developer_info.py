from io import BytesIO

from pyrogram.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pyrogram.raw.core import TLObject
from pyrogram import raw
from typing import List, Optional, Any


class SaveDeveloperInfo(TLObject):  # type: ignore
    __slots__: List[str] = ["vk_id", "name", "phone_number", "age", "city"]

    ID = 0x9a5f6e95
    QUALNAME = "functions.contest.SaveDeveloperInfo"

    def __init__(self, *, vk_id: int, name: str, phone_number: str, age: int, city: str) -> None:
        self.vk_id = vk_id  # int
        self.name = name  # string
        self.phone_number = phone_number  # string
        self.age = age  # int
        self.city = city  # string

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "SaveDeveloperInfo":
        # No flags
        
        vk_id = Int.read(b)
        
        name = String.read(b)
        
        phone_number = String.read(b)
        
        age = Int.read(b)
        
        city = String.read(b)
        
        return SaveDeveloperInfo(vk_id=vk_id, name=name, phone_number=phone_number, age=age, city=city)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.vk_id))
        
        b.write(String(self.name))
        
        b.write(String(self.phone_number))
        
        b.write(Int(self.age))
        
        b.write(String(self.city))
        
        return b.getvalue()
