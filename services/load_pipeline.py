from functools import lru_cache

import joblib
from pathlib import Path
from app.main import logger

ROOT = Path(__file__).resolve().parent.parent
pipeline_path = ROOT / "pipeline" / "SVC_pipeline.joblib"


@lru_cache(maxsize=1)
def load_pipeline():
    try:
        logger.info("Started - loading pipeline")
        pipeline = joblib.load(pipeline_path)
        logger.info("Finished - loading pipeline")
        return pipeline
    except Exception as e:
        logger.exception(f"Failed to lad pipeline: {e}")
        raise
