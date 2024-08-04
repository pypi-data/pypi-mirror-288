from datetime import datetime, UTC
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

import pytest

from wapchita.client import Wapchita

@pytest.fixture
def WAP_URL_BASE() -> str: return os.getenv("WAP_URL_BASE")
@pytest.fixture
def WAP_API_KEY() -> str: return os.getenv("WAP_API_KEY")
@pytest.fixture
def WAP_DEVICE_ID() -> str: return os.getenv("WAP_DEVICE_ID")
@pytest.fixture
def WAP_PHONE() -> str: return os.getenv("WAP_PHONE")
@pytest.fixture
def PHONE_TESTER() -> str: return os.getenv("PHONE_TESTER")

@pytest.fixture
def wapchita(WAP_API_KEY: str, WAP_DEVICE_ID: str) -> Wapchita:
    return Wapchita(tkn=WAP_API_KEY, device=WAP_DEVICE_ID)

@pytest.fixture
def path_data() -> Path:
    path_data_ = Path(__file__).parent / "data"
    path_data_.mkdir(exist_ok=True)
    return path_data_

@pytest.fixture
def TEXT_TEST() -> str:
    return f"Simple text message {datetime.now(tz=UTC)}"

@pytest.fixture
def PATH_IMG_PNG_TEST(path_data: Path) -> Path:
    return path_data / "michis.png"

@pytest.fixture
def PATH_IMG_JPEG_TEST(path_data: Path) -> Path:
    return path_data / "michis.jpeg"
