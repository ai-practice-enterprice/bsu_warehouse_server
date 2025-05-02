from fastapi.testclient import TestClient


def test_fake_customers(client: TestClient):
    response = client.get("/fake/customers?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_packages(client: TestClient):
    response = client.get("/fake/packages?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_locations(client: TestClient):
    response = client.get("/fake/locations?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_flights(client: TestClient):
    response = client.get("/fake/flights?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_cities(client: TestClient):
    response = client.get("/fake/cities?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_airplanes(client: TestClient):
    response = client.get("/fake/airplanes?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_airports(client: TestClient):
    response = client.get("/fake/airports?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_fake_airlines(client: TestClient):
    response = client.get("/fake/airlines?limit=5&locale=nl_BE")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
