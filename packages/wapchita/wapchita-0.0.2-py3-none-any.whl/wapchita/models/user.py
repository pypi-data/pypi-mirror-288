from typing import Type, TypeVar

from pydantic import BaseModel

from wapchita.request import search_chat

__all__ = ["WapUser"]

T_WapUser = TypeVar("T_WapUser", bound="WapUser")

class WapUser(BaseModel):
    wid: str
    displayName: str    # TODO: Mover a snake con alias.
    phone: str
    
    @classmethod
    def from_phone(cls: Type[T_WapUser], *, tkn: str, phone: str, device_id: str) -> Type[T_WapUser]:
        response_search_chat = search_chat(tkn=tkn, phone=phone, device_id=device_id)
        #print(response_search_chat.json())     # TODO: Tira 500. y no tiene [0].
        contact = response_search_chat.json()[0]["contact"]
        return cls(**contact)
