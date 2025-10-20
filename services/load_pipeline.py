import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

pipeline_path = ROOT / "pipeline" / "SVC_pipeline.joblib"
pipeline = joblib.load(pipeline_path)


# masz juz teraz zrobiny pipeline kotry mozesz pobrac  i robic z niego predyckje
# nie wiem:
# - jak ułożyc pliki i fodlery
# - jakie pliki i foldery są potrzebne
# - jak i gdzie zrobic schemt danych z Pydantic
# - jak i gdzie napsiac fastapi
