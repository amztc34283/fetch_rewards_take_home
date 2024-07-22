from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_process_receipt_happy_path():
    response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
        }
    )
    assert response.status_code == 200
    assert 'id' in response.json()

def test_process_receipt_no_items():
    response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [],
            "total": "35.35"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The receipt is invalid"}

def test_process_receipt_data_validation():
    response = client.post(
        "/receipts/process",
        json={
            "retailer": "Target//",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "total": "35.35"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "The receipt is invalid"}

def test_get_points_with_unknown_id():
    with TestClient(app) as client: # initialize datastore
        response = client.get(f"/receipts/dummy/points")
        assert response.status_code == 404
        assert response.json() == {"detail": "No receipt found for that id"}

def test_get_points_with_known_id():
    with TestClient(app) as client: # initialize datastore
        response = client.post(
            "/receipts/process",
            json={
                "retailer": "Target",
                "purchaseDate": "2022-01-01",
                "purchaseTime": "13:01",
                "items": [
                    {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                    },{
                    "shortDescription": "Emils Cheese Pizza",
                    "price": "12.25"
                    },{
                    "shortDescription": "Knorr Creamy Chicken",
                    "price": "1.26"
                    },{
                    "shortDescription": "Doritos Nacho Cheese",
                    "price": "3.35"
                    },{
                    "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                    "price": "12.00"
                    }
                ],
                "total": "35.35"
            }
        )
        response = client.get(f"/receipts/{response.json()['id']}/points")
        assert response.status_code == 200
        assert response.json() == {"points": 28}

def test_unknown_path():
    response = client.get("/unknown")
    assert response.status_code == 404