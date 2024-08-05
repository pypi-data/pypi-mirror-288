"""
- FIXME: Realmente no necesito el device, solo su ID y el número, pero
quizás otros datos como el nombre y demás puedan ayudarme en el futuro.
"""
from typing import List
from pathlib import Path

from requests import Response

from wapchita.typings import Priority, PRIORITY_DEFAULT, SortChats, SORTCHATS_DEFAULT
from wapchita.models.device import WapDevice
from wapchita.models.user import WapUser
from wapchita.request_wap import RequestWap


class Wapchita:
    def __init__(self, *, tkn: str, device: WapDevice | str | Path):
        self._request_wap = RequestWap(tkn=tkn, device=device)
    
    @property
    def request_wap(self) -> RequestWap:
        return self._request_wap

    @property
    def device(self) -> WapDevice:
        return self.request_wap.device
    
    @property
    def device_id(self) -> WapDevice:
        return self.request_wap.device_id
    
    def user_from_phone(self, *, phone: str) -> WapUser:
        r = self.request_wap.contacts(phone=phone)
        if r.status_code != 200:
            raise Exception(f"Error al buscar usuario, documentar. {r.json()}")
        return WapUser(**self.request_wap.contacts(phone=phone).json())
    
    def send_message(self, *, phone: str, message: str = "", file_id: str = None, priority: Priority = PRIORITY_DEFAULT) -> Response:
        return self.request_wap.send_message(phone=phone, message=message, file_id=file_id, priority=priority)

    def edit_message(self, *, message_wid: str, text: str) -> Response:
        return self.request_wap.edit_message(message_wid=message_wid, text=text)

    def get_chats(self, *, user_wid: str, sort_: SortChats = SORTCHATS_DEFAULT) -> Response:
        return self.request_wap.get_chats(user_wid=user_wid, sort_=sort_)

    def download_file(self, *, file_id: str) -> Response:
        return self.request_wap.download_file(file_id=file_id)

    def upload_file(self, *, path_file: Path) -> Response:
        return self.request_wap.upload_file(path_file=path_file)

    def update_chat_labels(self, *, user_wid: str, labels: List[str] = None) -> Response:
        return self.request_wap.update_chat_labels(user_wid=user_wid, labels=labels)
    
    def upload_send_img(self, *, path_img: Path, phone: str) -> str:
        response_upload = self.upload_file(path_file=path_img)
        try:    # FIXME: Si el fichero existe tira un 400, por que te dice que uses el existente, y retorna el file_id.
            file_id = response_upload.json()[0]["id"]
        except Exception as e:
            file_id = response_upload.json()["meta"]["file"]
        self.send_message(phone=phone, file_id=file_id)
        return file_id
