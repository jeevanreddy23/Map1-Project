from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_project_save_and_geojson_load() -> None:
    project = {
        "id": "test-project",
        "name": "Test Site Investigation",
        "geojson": {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [151.2093, -33.8688],
                    },
                    "properties": {
                        "id": "feature-1",
                        "feature_type": "borehole",
                        "label": "BH01",
                        "borehole_id": "BH01",
                        "latitude": -33.8688,
                        "longitude": 151.2093,
                    },
                }
            ],
        },
    }

    save_response = client.put("/api/projects/test-project", json=project)
    assert save_response.status_code == 200

    geojson_response = client.get("/api/projects/test-project/geojson")
    assert geojson_response.status_code == 200
    geojson = geojson_response.json()
    assert geojson["type"] == "FeatureCollection"
    assert geojson["features"][0]["properties"]["borehole_id"] == "BH01"


def test_two_point_transform() -> None:
    calibration = {
        "overlay_id": "overlay-1",
        "coordinate_system": "WGS84",
        "points": [
            {
                "pixel_x": 0,
                "pixel_y": 0,
                "longitude": 151.0,
                "latitude": -33.0,
            },
            {
                "pixel_x": 100,
                "pixel_y": 0,
                "longitude": 151.1,
                "latitude": -33.0,
            },
        ],
    }

    calibration_response = client.post("/api/calibrations", json=calibration)
    assert calibration_response.status_code == 200
    payload = calibration_response.json()
    assert payload["method"] == "two_point_similarity"

    transform_response = client.post(
        "/api/transform/pixel-to-coordinate",
        json={
            "calibration_id": payload["id"],
            "pixel_x": 50,
            "pixel_y": 0,
        },
    )
    assert transform_response.status_code == 200
    transformed = transform_response.json()
    assert round(transformed["longitude"], 6) == 151.05
    assert round(transformed["latitude"], 6) == -33.0

