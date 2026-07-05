from unittest.mock import patch

from app.services.email_service import send_fake_email
from app.services.external_service import get_weather_sync


def test_email_service_mocked():
    with patch("app.services.email_service.send_fake_email") as mock_email:
        mock_email("Test task")

        mock_email.assert_called_once_with("Test task")


def test_external_weather_sync_mocked():
    with patch("app.services.external_service.get_weather_sync") as mock_weather:
        mock_weather.return_value = {
            "city": "Nablus",
            "temperature": 22,
            "condition": "Sunny",
            "type": "sync"
        }

        result = get_weather_sync()

        assert result["city"] == "Nablus"
        assert result["type"] == "sync"