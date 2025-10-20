from loguru import logger
from fastapi import FastAPI, Request
from .schemas import PredictionResults, InputSchema, column_map
from services.load_pipeline import pipeline
import pandas as pd
import sys
from uuid import uuid4
import time

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


@app.middleware("http")
async def log_requests(request: Request, call_next):
    id = str(uuid4())
    with logger.contextualize(request_id=id):
        start_time = time.perf_counter()
        logger.info(f"Started {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(f"Exception occured {request.method} {request.url} - {e}")
        finally:
            elapsed_time = (time.perf_counter() - start_time) * 1000
            logger.info(
                f"⬅️ Completed {request.method} {request.url.path} "
                f"with status={getattr(response, 'status_code', 'N/A')} "
                f"in {elapsed_time:.2f}ms"
            )
        return response


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

    pred = pipeline.predict(X)[0]
    proba = pipeline.predict_proba(X)[0, 0]
    return PredictionResults(prediction=pred, probability=proba)
