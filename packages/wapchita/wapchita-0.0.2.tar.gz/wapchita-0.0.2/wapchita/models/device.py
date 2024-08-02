from typing import Type, TypeVar, Optional
import logging
logger = logging.getLogger(__name__)

from pydantic import BaseModel

from wapchita.request import device_by_id

__all__ = ["WapDevice"]

T_WapDevice = TypeVar("T_WapDevice", bound="WapDevice")

class WapDevice(BaseModel):
    id: str
    phone: str
    alias: str
    wid: Optional[str] = None
    version: Optional[int] = None
    plan: Optional[str] = None

    @classmethod
    def from_device_id(cls: Type[T_WapDevice], *, tkn: str, device_id: str) -> T_WapDevice:
        response = device_by_id(tkn=tkn, device_id=device_id)
        device = cls(**response.json())
        return device
