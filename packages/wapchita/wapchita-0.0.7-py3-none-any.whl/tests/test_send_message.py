import pytest

from wapchita.client import Wapchita

def test_send_message_text(wapchita: Wapchita, PHONE_TESTER: str, TEXT_TEST: str) -> None:
    r = wapchita.send_message(phone=PHONE_TESTER, message=TEXT_TEST)
    assert r.status_code == 201

# def test_send_message_img(wapchita: Wapchita, PHONE_TESTER: str, TEXT_TEST: str) -> None:
#     r = wapchita.send_message(phone=PHONE_TESTER, message=TEXT_TEST)
#     assert r.status_code == 201
# 
# def test_send_message_text(wapchita: Wapchita, PHONE_TESTER: str, TEXT_TEST: str) -> None:
#     r = wapchita.send_message(phone=PHONE_TESTER, message=TEXT_TEST)
#     assert r.status_code == 201
# 
# def test_send_message_text(wapchita: Wapchita, PHONE_TESTER: str, TEXT_TEST: str) -> None:
#     r = wapchita.send_message(phone=PHONE_TESTER, message=TEXT_TEST)
#     assert r.status_code == 201