from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

Timezone = Union["raw.types.Timezone"]


# noinspection PyRedeclaration
class Timezone:  # type: ignore
    QUALNAME = "pyrogram.raw.base.Timezone"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
