import os

WAP_URL_BASE = "WAP_URL_BASE"
V1 = "v1"

def url_base() -> str:
    return os.getenv(WAP_URL_BASE)

def url_device_by_id(*, device_id: str) -> str:
    return f"{url_base()}/{V1}/devices/{device_id}"

def url_send_message() -> str:
    """ https://app.shock.uy/docs/#tag/Messages/operation/createMessage"""
    return f"{url_base()}/{V1}/messages"

def url_edit_message(*, device_id: str, message_wid: str) -> str:
    return f"{url_base()}/{V1}/chat/{device_id}/messages/{message_wid}"

def url_search_chats(*, device_id: str) -> str:
    return f"{url_base()}/{V1}/chat/{device_id}/chats"

def url_get_chats(*, device_id: str) -> str:
    return f"{url_base()}/{V1}/chat/{device_id}/messages"

def url_download_file(*, device_id: str, file_id: str) -> str:
    return f"{url_base()}/{V1}/chat/{device_id}/files/{file_id}/download"

def url_upload_file() -> str:
    return f"{url_base()}/{V1}/files"

def url_update_chat_labels(*, device_id: str, user_wid: str) -> str:
    return f"{url_base()}/{V1}/chat/{device_id}/chats/{user_wid}/labels"
