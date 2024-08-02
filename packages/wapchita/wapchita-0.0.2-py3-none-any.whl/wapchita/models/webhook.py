from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel, Field

from wapchita.models.device import WapDevice
from wapchita.models.types import MsgType

__all__ = ["WapWebhookBody"]


class WapEvents(BaseModel):
    sent: Optional[dict] = None

class WapLinks(BaseModel):
    message: str
    chat: str
    contact: str
    chatMessages: str
    device: str
    agent: Optional[str] = None

class WapMeta(BaseModel):
    rtl: bool
    containsEmoji: bool
    isGif: bool
    isStar: bool
    isGroup: bool
    isChannel: bool
    isForwarded: bool
    isEphemeral: bool
    isNotification: bool
    isLive: bool
    isBroadcast: bool
    isBizNotification: bool
    isDoc: bool
    isLinkPreview: bool
    isPSA: bool
    isRevoked: bool
    isUnreadType: bool
    isFailed: bool
    notifyName: str
    source: str
    via: Optional[str] = None
    isFirstMessage: bool

class WapStats(BaseModel):
    notes: int
    localMessages: int
    inboundMessages: int
    outboundMessages: int

class WapOwner(BaseModel):
    agent: Optional[str]
    assigner: Optional[str] = None
    assignedAt: Optional[str] = None

class WapChat(BaseModel):
    id: str
    name: Optional[str] = None
    date: Optional[str] = None
    type: str
    status: str
    waStatus: str
    statusUpdatedAt: Optional[str] = None
    firstMessageAt: str
    lastMessageAt: str
    lastOutboundMessageAt: Optional[str] = None
    lastInboundMessageAt: Optional[str] = None
    lastAutoReply: None                 # ---> TODO
    lastAutoReplyAt: None               # ---> TODO
    stats: WapStats
    labels: List[str]
    owner: WapOwner
    contact: dict                       # ---> TODO
    links: dict                         # ---> TODO

class WapData(BaseModel):
    id: str
    type: MsgType
    flow: str
    status: str
    ack: str
    agent: Optional[str] = None
    from_: str = Field(alias="from")
    fromNumber: str
    to: str
    toNumber: str
    date: datetime
    timestamp: int
    body: Optional[str] = None
    chat: WapChat
    events: WapEvents
    meta: WapMeta
    links: WapLinks


class WapWebhookBody(BaseModel):
    id: str
    object: str
    event: str
    created: int
    device: WapDevice
    data: WapData

    @property
    def message_id(self) -> str:
        return self.id

    @property
    def text(self) -> str | None:
        return self.data.body

    @property
    def labels(self) -> List[str]:
        """ Etiquetas configurables del lado de Wapchita."""
        return self.data.chat.labels
    
    @property
    def device_id(self) -> str:
        return self.device.id
    
    @property
    def device_phone(self) -> str:
        return self.device.phone
    
    @property
    def from_phone(self) -> str:
        return self.data.fromNumber
    
    @property
    def to_phone(self) -> str:
        return self.data.toNumber

    #----------Categoría del Mensaje----------
    @property
    def is_bot_request(self) -> bool:
        """ Retorna True la solicitud viene del propio bot."""
        return self.device_phone == self.from_phone

    @property
    def is_text(self) -> bool:
        return self.data.type == "text"
    
    @property
    def is_image(self) -> bool:
        return self.data.type == "image"
    
    @property
    def is_sticker(self) -> bool:
        return self.data.type == "sticker"
    
    @property
    def is_video(self) -> bool:
        return self.data.type == "video"
    
    @property
    def is_location(self) -> bool:
        return self.data.type == "location"
    
    @property
    def is_audio(self) -> bool:
        return self.data.type == "audio"
    
    @property
    def is_document(self) -> bool:
        return self.data.type == "document"
    
    @property
    def is_contacts(self) -> bool:
        return self.data.type == "contacts"
    #----------Categoría del Mensaje----------
