from typing import Optional
import logging
logger = logging.getLogger(__name__)

from pydantic import BaseModel

__all__ = ["WapDevice"]


class WapDevice(BaseModel):
    id: str
    phone: str
    alias: str
    wid: Optional[str] = None
    version: Optional[int] = None
    plan: Optional[str] = None
