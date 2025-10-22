import pandas as pd
import pytest
import numpy as np
from services.load_pipeline import pipeline_path, load_pipeline


@pytest.fixture(scope="session")  # Load pipeline only once per test session
def pipeline():
    pipeline = load_pipeline()
    return pipeline


@pytest.fixture()
def data_to_predict_on_pipeline() -> pd.DataFrame:
    data = {
        "mean radius": 2.44,
        "mean texture": 323,
        "mean smoothness": 34.2,
        "mean compactness": 234,
        "mean concavity": 3.4,
        "mean concave points": 4,
        "mean symmetry": 1.09,
        "mean fractal dimension": 34,
        "texture error": 3,
        "area error": 1,
        "smoothness error": 4,
        "compactness error": 3.332,
        "concavity error": 2,
        "symmetry error": 4,
        "fractal dimension error": 43,
        "worst texture": 22,
        "worst smoothness": 56.1,
        "worst compactness": 2.34,
        "worst symmetry": 34.3,
        "worst fractal dimension": 45,
    }
    return pd.DataFrame([data])  # turn it into one row multiple columns


def test_pipeline_if_exists():
    assert pipeline_path.exists()


def test_pipeline(data_to_predict_on_pipeline, pipeline):
    assert pipeline.predict(data_to_predict_on_pipeline) == np.array([1])
    proba = pipeline.predict_proba(data_to_predict_on_pipeline)
    assert proba.shape == (1, 2)
    assert isinstance(proba[0, 0], float)
    assert isinstance(proba[0, 1], float)
