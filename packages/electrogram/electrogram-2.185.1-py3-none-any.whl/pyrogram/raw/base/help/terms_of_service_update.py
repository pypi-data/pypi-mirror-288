from typing import Union
from pyrogram import raw
from pyrogram.raw.core import TLObject

TermsOfServiceUpdate = Union["raw.types.help.TermsOfServiceUpdate", "raw.types.help.TermsOfServiceUpdateEmpty"]


# noinspection PyRedeclaration
class TermsOfServiceUpdate:  # type: ignore
    QUALNAME = "pyrogram.raw.base.help.TermsOfServiceUpdate"

    def __init__(self):
        raise TypeError("Base types can only be used for type checking purposes")
