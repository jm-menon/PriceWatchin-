from workers.scraper.clients import health_check, fetch_product
from workers.scraper.repository import get_all_products
import requests

def test_health_check(mocker):

    mock_response = mocker.Mock()
    mock_response.status_code = 200

    mocker.patch(
        "workers.scraper.clients.requests.get",
        return_value=mock_response
    )

    assert health_check("http://localhost:8001") is True


def test_health_check_failure(mocker):

    mocker.patch(
        "workers.scraper.clients.requests.get",
        side_effect=requests.exceptions.ConnectionError
    )

    assert health_check("http://localhost:8001") is False


def test_fetch_product(mocker):

    fake = mocker.Mock()

    fake.json.return_value = {
        "product_id":1,
        "base_price":999,

    }

    fake.raise_for_status.return_value = None

    mocker.patch(
        "workers.scraper.clients.requests.get",
        return_value=fake
    )

    product = fetch_product(
        "http://localhost:8001",
        1,
        1
    )

    assert product["base_price"] == 999
    assert product["product_id"] == 1

def test_get_all_products(mocker):

    fake_rows = mocker.Mock()
    fake_rows.fetchall.return_value = [
        (1, "iPhone 16"),
        (2, "Samsung Galaxy S26")
    ]

    fake_session = mocker.Mock()
    fake_session.execute.return_value = fake_rows

    mocker.patch(
        "workers.scraper.repository.Session",
        return_value=fake_session
    )

    result = get_all_products()

    assert result == [
        (1, "iPhone 16"),
        (2, "Samsung Galaxy S26")
    ]

    fake_session.execute.assert_called_once()