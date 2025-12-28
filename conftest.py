import pytest

@pytest.fixture
def base_url():
    return "https://api.openweathermap.org/data/2.5"

@pytest.fixture
def api_key():
    return "OPENWEATHER_API_KEY"
