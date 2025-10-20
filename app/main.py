from loguru import logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .schemas import PredictionResults, InputSchema, column_map
from services.load_pipeline import pipeline
import pandas as pd
import sys
from uuid import uuid4
import time
from services.data_manager import convert_pydantic_model_to_dict, convert_dict_to_pandas_df,map_column_names_to_pipeline_requrements

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
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"}
            )
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
    input_dict = convert_pydantic_model_to_dict(input_data)
    data_df = convert_dict_to_pandas_df(input_dict) # 1-row DataFrame with correct columns - pipleine was trained on dataframe
    map_column_names_to_pipeline_requrements(data_df)

    pred = pipeline.predict(data_df)[0]
    proba = pipeline.predict_proba(data_df)[0, 0]
    return PredictionResults(prediction=pred, probability=proba)
