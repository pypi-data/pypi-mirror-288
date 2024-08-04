import logging
logger = logging.getLogger(__name__)

import requests
from requests import Response
import tenacity
from tenacity import stop_after_attempt, wait_exponential

from wapchita.request_wap.urls import url_get_chats
from wapchita.request_wap.headers import get_headers
from wapchita.typings import SortChats, SORTCHATS_DEFAULT


@tenacity.retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=1, max=60))
def get_chats(
        *,
        tkn: str,
        device_id: str,
        user_wid: str,
        sort_: SortChats = SORTCHATS_DEFAULT
    ) -> Response:
    url = url_get_chats(device_id=device_id)
    params = {"chat": user_wid, "sort": sort_}#, "end": "my_message_id"}
    r = requests.get(url=url, headers=get_headers(tkn=tkn), params=params)
    if r.status_code >= 500:
        _msg = "Error inesperado de wapchita. Sin causa aparente, se reintenta."
        logger.warning(_msg)
        raise Exception(_msg)
    return r
