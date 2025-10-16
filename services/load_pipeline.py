import joblib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

pipeline_path = ROOT/"pipeline"/"SVC_pipeline.joblib"
pipeline = joblib.load(pipeline_path)



