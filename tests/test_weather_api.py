import pytest
import requests
from jsonschema import validate, ValidationError

# -----------------------------
# JSON Schema for weather API
# -----------------------------
weather_schema = {
    "type": "object",
    "properties": {
        "weather": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "description": {"type": "string"},
                    "main": {"type": "string"}
                },
                "required": ["description", "main"]
            }
        },
        "main": {
            "type": "object",
            "properties": {
                "temp": {"type": "number"},
                "humidity": {"type": "number"}
            },
            "required": ["temp", "humidity"]
        },
        "name": {"type": "string"}
    },
    "required": ["weather", "main", "name"]
}

# -----------------------------
# Helper function
# -----------------------------
def get_weather_data(base_url, api_key, lat, lon):
    params = {"lat": lat, "lon": lon, "appid": api_key}
    response = requests.get(f"{base_url}/weather", params=params)
    assert response.status_code == 200
    return response.json()

# -----------------------------
# Single City Test
# -----------------------------
def test_weather_riyadh(base_url, api_key):
    data = get_weather_data(base_url, api_key, 24.7136, 46.6753)

    # Schema validation with pass/fail print
    try:
        validate(instance=data, schema=weather_schema)
        print("\n""✅ JSON Schema Validation PASSED")
    except ValidationError as e:
        print("\n""❌ JSON Schema Validation FAILED")
        print("Error:", e)
        raise e

    # Temperature in Celsius
    temp_c = data["main"]["temp"] - 273.15

    print("\nCity Name:", data.get('name'))
    print(f"Temperature: {temp_c:.2f} °C")
    print(f"Weather Description: {data['weather'][0]['description']}")

# -----------------------------
# Parametrized Test for Multiple Cities
# -----------------------------
@pytest.mark.parametrize("lat, lon, city", [
    (24.7136, 46.6753, "Riyadh"),
    (21.3891, 39.8579, "Makkah al Mukarramah"),
    (21.4858, 39.1925, "Jeddah")
])
def test_weather_multiple(base_url, api_key, lat, lon, city):
    data = get_weather_data(base_url, api_key, lat, lon)

    # Schema validation with print
    try:
        validate(instance=data, schema=weather_schema)
        print(f"✅ JSON Schema Validation PASSED for {city}")
    except ValidationError as e:
        print(f"❌ JSON Schema Validation FAILED for {city}")
        print("Error:", e)
        raise e

    # Temperature in Celsius
    temp_c = data["main"]["temp"] - 273.15
    print(f"{city} Temperature: {temp_c:.2f} °C")
    print(f"Weather: {data['weather'][0]['description']}")

    assert data["name"] == city

# -----------------------------
# Negative Test: Invalid API Key
# -----------------------------
def test_invalid_api_key(base_url):
    params = {"lat": 24.7136, "lon": 46.6753, "appid": "wrong_key"}
    response = requests.get(f"{base_url}/weather", params=params)
    assert response.status_code == 401  # Unauthorized
    print("✅ Invalid API key correctly returned 401")
