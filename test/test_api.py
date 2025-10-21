from fastapi.testclient import TestClient
import pytest

from app.main import app
from app.schemas import InputSchema

client = TestClient(app)


@pytest.fixture
def valid_data_to_predict() -> dict:
    return {
        "mean_radius": 2.44,
        "mean_texture": 323,
        "mean_smoothness": 34.2,
        "mean_compactness": 234,
        "mean_concavity": 3.4,
        "mean_concave_points": 4,
        "mean_symmetry": 1.09,
        "mean_fractal_dimension": 34,
        "texture_error": 3,
        "area_error": 1,
        "smoothness_error": 4,
        "compactness_error": 3.332,
        "concavity_error": 2,
        "symmetry_error": 4,
        "fractal_dimension_error": 43,
        "worst_texture": 22,
        "worst_smoothness": 56.1,
        "worst_compactness": 2.34,
        "worst_symmetry": 34.3,
        "worst_fractal_dimension": 45,
    }


@pytest.fixture
def invalid_data_to_predict() -> dict:
    return {
        "mean_radius": 2.44,
        "mean_texture": 323,
        "mean_smoothness": 34.2,
        "mean_compactness": 234,
        "mean_concavity": 3.4,
        "mean_concave_points": 4,
        "mean_symmetry": 1.09,
        "mean_fractal_dimension": 34,
        "texture_error": 3,
        "area_error": 1,
        "smoothness_error": 4,
        "compactness_error": 3.332,
        "concavity_error": 2,
        "symmetry_error": 4,
        "fractal_dimension_error": 43,
        "worst_texture": 22,
        "worst_smoothness": 56.1,
        "worst_compactness": 2.34,
        "worst_symmetry": 34.3,
        # "worst_fractal_dimension": 45,
    }


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_valid_data(valid_data_to_predict):
    response = client.post("/predict", json=valid_data_to_predict)
    assert response.status_code == 200
    pred = response.json()["prediction"]
    proba = response.json()["probability"]
    assert pred in {0, 1}
    assert type(float)
    assert 0 <= proba <= 1


def test_predict_invalid_data(invalid_data_to_predict):
    response = client.post("/predict", json=invalid_data_to_predict)
    assert response.status_code == 422
