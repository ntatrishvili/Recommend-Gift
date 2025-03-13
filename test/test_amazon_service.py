from unittest import mock
import pytest
from app.services.amazon_service import search_amazon


@pytest.mark.asyncio
@mock.patch("app.services.amazon_service.requests.get")
async def test_search_amazon_success(mock_get):
    mock_response = mock.Mock()
    expected_data = {
        "data": {
            "products": [
                {
                    "product_price": "20.00",
                    "product_url": "http://example.com/product1",
                    "product_photo": "http://example.com/product1.jpg",
                    "product_star_rating": "4.5",
                },
                {
                    "product_price": "15.00",
                    "product_url": "http://example.com/product2",
                    "product_photo": "http://example.com/product2.jpg",
                    "product_star_rating": "4.0",
                },
            ]
        }
    }
    mock_response.status_code = 200
    mock_response.json.return_value = expected_data
    mock_get.return_value = mock_response

    price, url, photo = await search_amazon("test query", 25)

    assert price == "20.00"
    assert url == "http://example.com/product1"
    assert photo == "http://example.com/product1.jpg"


@pytest.mark.asyncio
@mock.patch("app.services.amazon_service.requests.get")
async def test_search_amazon_no_products(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": {"products": []}}
    mock_get.return_value = mock_response

    price, url, photo = await search_amazon("test query", 25)

    assert price is None
    assert url is None
    assert photo is None


@pytest.mark.asyncio
@mock.patch("app.services.amazon_service.requests.get")
async def test_search_amazon_no_data(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    price, url, photo = await search_amazon("test query", 25)

    assert price is None
    assert url is None
    assert photo is None


@pytest.mark.asyncio
@mock.patch("app.services.amazon_service.requests.get")
async def test_search_amazon_api_failure(mock_get):
    mock_response = mock.Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    price, url, photo = await search_amazon("test query", 25)

    assert price is None
    assert url is None
    assert photo is None
