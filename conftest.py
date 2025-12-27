import pytest

@pytest.fixture
def base_url():
    return "https://api.openweathermap.org/data/2.5"

@pytest.fixture
def api_key():
    return "4e68f9c659ffbe00b864d8f621eeced3"
