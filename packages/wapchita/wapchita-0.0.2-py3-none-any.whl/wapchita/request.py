from typing import Literal, List
from pathlib import Path
from requests import Response
import requests
import logging
logger = logging.getLogger(__name__)

import tenacity
from tenacity import stop_after_attempt, wait_exponential

from wapchita.url import (
    url_device_by_id, url_send_message, url_search_chats,
    url_get_chats, url_edit_message, url_download_file, url_upload_file,
    url_update_chat_labels
)
from wapchita.headers import get_headers, get_headers_app_json

PRIORITY_DEFAULT = "normal"
Priority = Literal["low", "normal", "high", "urgent"]
SORTCHATS_DEFAULT = "date:desc"
SortChats = Literal["date:asc", "date:desc"]

def device_by_id(*, tkn: str, device_id: str) -> Response:
    url = url_device_by_id(device_id=device_id)
    return requests.get(url=url, headers=get_headers(tkn=tkn))

def send_message(*, tkn: str, phone: str, message: str = "", file_id: str = None, priority: Priority = PRIORITY_DEFAULT) -> Response:
    url = url_send_message()
    json_ = {"phone": phone, "message": message, "priority": priority}
    if file_id is not None:
        json_["media"] = {"file": file_id}
    return requests.post(url=url, json=json_, headers=get_headers_app_json(tkn=tkn))

def edit_message(*, tkn: str, device_id: str, message_wid: str, text: str) -> Response:
    """ Tiempo máximo de 20 minutos."""
    url = url_edit_message(device_id=device_id, message_wid=message_wid)
    return requests.patch(url=url, json={"message": text}, headers=get_headers_app_json(tkn=tkn))


def search_chat(*, tkn: str, phone: str, device_id: str) -> Response:
    """
    - TODO: Ver search_chats en plural.
    - TODO: Ver si se puede filtrar por fecha, diferencia de tiempo entre mensajes, algo asi.
    - https://app.shock.uy/docs/#tag/Chats/operation/getDeviceChats
    """
    url = url_search_chats(device_id=device_id)
    return requests.get(url=url, headers=get_headers(tkn=tkn), params={"phone": phone})

@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=60))
def get_chats(*, tkn: str, device_id: str, user_wid: str, sort_: SortChats = SORTCHATS_DEFAULT) -> Response:
    url = url_get_chats(device_id=device_id)
    params = {"chat": user_wid, "sort": sort_}#, "end": "my_message_id"}
    r = requests.get(url=url, headers=get_headers(tkn=tkn), params=params)
    if r.status_code >= 500:
        _msg = "Error inesperado de wapchita. Sin causa aparente, se reintenta."
        logger.warning(_msg)
        raise Exception(_msg)
    return r

def download_file(*, tkn: str, device_id: str, file_id: str) -> Response:
    """ https://app.shock.uy/docs/#tag/Chat-Files/operation/downloadDeviceFileDetails"""
    url = url_download_file(device_id=device_id, file_id=file_id)
    return requests.get(url=url, headers=get_headers(tkn=tkn))

def upload_file(*, tkn: str, path_file: Path) -> Response:
    """ TODO: Se pueden cargar varios productos en simultáneo?."""
    url = url_upload_file()
    files = {"file": open(path_file, 'rb')}
    #querystring = {"reference":"optional-reference-id"}
    return requests.post(url=url, files=files, headers=get_headers(tkn=tkn))#, params=querystring)

def update_chat_labels(*, tkn: str, device_id: str, user_wid: str, labels: List[str] = None) -> Response:
    url = url_update_chat_labels(device_id=device_id, user_wid=user_wid)
    if labels is None:
        labels = []
    return requests.patch(url=url, json=labels, headers=get_headers_app_json(tkn=tkn))
