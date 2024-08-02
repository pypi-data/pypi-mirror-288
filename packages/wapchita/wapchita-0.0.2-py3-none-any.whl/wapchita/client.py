"""
- FIXME: Realmente no necesito el device, solo su ID y el número, pero
quizás otros datos como el nombre y demás puedan ayudarme en el futuro.
"""
from typing import List
from pathlib import Path

from requests import Response

from wapchita.models.device import WapDevice
from wapchita.models.user import WapUser
from wapchita.request import (
    PRIORITY_DEFAULT, SORTCHATS_DEFAULT, Priority, SortChats,
    send_message, edit_message, get_chats, download_file,
    upload_file, update_chat_labels
)

class Wapchita:
    def __init__(self, *, tkn: str, device_id: str):
        self._tkn = tkn
        self._device_id = device_id
        self._device: WapDevice = None
    
    @property
    def tkn(self) -> str:
        return self._tkn
    
    @property
    def device_id(self) -> str:
        return self._device_id
    
    @property
    def device(self) -> WapDevice:
        if self._device is None:
            # FIXME: Que lo levante de un .json.
            self._device = WapDevice.from_device_id(tkn=self.tkn, device_id=self.device_id)
        return self._device
        
    def user_from_phone(self, *, phone: str) -> WapUser:
        return WapUser.from_phone(tkn=self.tkn, phone=phone, device_id=self.device.id)
    
    def send_message(self, *, phone: str, message: str = "", file_id: str = None, priority: Priority = PRIORITY_DEFAULT) -> Response:
        return send_message(tkn=self.tkn, phone=phone, message=message, file_id=file_id, priority=priority)

    def edit_message(self, *, message_wid: str, text: str) -> Response:
        return edit_message(tkn=self.tkn, device_id=self.device.id, message_wid=message_wid, text=text)

    def get_chats(self, *, user_wid: str, sort_: SortChats = SORTCHATS_DEFAULT) -> Response:
        return get_chats(tkn=self.tkn, device_id=self.device.id, user_wid=user_wid, sort_=sort_)

    def download_file(self, *, file_id: str) -> Response:
        return download_file(tkn=self.tkn, device_id=self.device.id, file_id=file_id)

    def upload_file(self, *, path_file: Path) -> Response:
        return upload_file(tkn=self.tkn, path_file=path_file)

    def update_chat_labels(self, *, user_wid: str, labels: List[str] = None) -> Response:
        return update_chat_labels(tkn=self.tkn, device_id=self.device.id, user_wid=user_wid, labels=labels)

    def upload_send_img(self, *, path_img: Path, phone: str) -> str:
        response_upload = self.upload_file(path_file=path_img)
        try:    # FIXME: Si el fichero existe tira un 400, por que te dice que uses el existente, y retorna el file_id.
            file_id = response_upload.json()[0]["id"]
        except Exception as e:
            file_id = response_upload.json()["meta"]["file"]
        self.send_message(phone=phone, file_id=file_id)
        return file_id
