import pytest

from wapchita.client import Wapchita
from wapchita.models.user import WapUser

def test_get_user(wapchita: Wapchita, PHONE_TESTER: str) -> None:
    user = wapchita.user_from_phone(phone=PHONE_TESTER)
    assert isinstance(user, WapUser) and user.phone == PHONE_TESTER
