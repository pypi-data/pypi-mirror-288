from typing import Type, TypeVar, Literal, Optional, Any
from datetime import datetime

from pydantic import BaseModel

from wapchita.models._extras._user import WapUserLocInfo, WapMetaUser
from wapchita.models.device import WapDevice

__all__ = ["WapUser"]

T_WapUser = TypeVar("T_WapUser", bound="WapUser")

class WapUser(BaseModel):
    wid: str                        # TODO: Revisar que phone2wid() == wid
    phone: str
    type: Literal["user"]
    displayName: str
    shortName: Optional[str] = None
    syncedAt: datetime
    createdBy: Optional[Any]        # TODO: Ver.
    locationInfo: WapUserLocInfo
    info: dict
    meta: WapMetaUser
    metadata: list
    device: WapDevice
    
    @classmethod
    def from_phone(cls: Type[T_WapUser], *, tkn: str, phone: str, device_id: str) -> Type[T_WapUser]:
        pass
        #response_search_chat = search_chat(tkn=tkn, phone=phone, device_id=device_id)
        ##print(response_search_chat.json())     # TODO: Tira 500. y no tiene [0].
        #try:
        #    contact = response_search_chat.json()[0]["contact"]
        #except:
        #    print(response_search_chat.status_code)
        #    return ""
        #return cls(**contact)
