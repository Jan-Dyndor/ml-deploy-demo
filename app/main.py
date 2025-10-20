from loguru import logger
from fastapi import FastAPI
from .schemas import PredictionResults, InputSchema, column_map
from services.load_pipeline import pipeline
import pandas as pd
import sys

logger.add(
    sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level:<7}</level> "
    "| <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
    "| id={extra[request_id]} - <level>{message}</level>",
    colorize=True,
    backtrace=True,
    diagnose=True,
    enqueue=True,
)


app = FastAPI()


@app.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResults)
async def predict(input_data: InputSchema) -> PredictionResults:
    input_dict = input_data.model_dump()
    X = pd.DataFrame(
        [input_dict]
    )  # 1-row DataFrame with correct columns - pipleine was trained on dataframe
    X.rename(
        columns=column_map, inplace=True
    )  # I created model with mean_radius but pipeline was trained on mean radius
    # it does not know what `_` is
    print(X)
    pred = pipeline.predict(X)[0]
    print(pred)
    proba = pipeline.predict_proba(X)[0, 0]
    print(proba)
    return PredictionResults(prediction=pred, probability=proba)
