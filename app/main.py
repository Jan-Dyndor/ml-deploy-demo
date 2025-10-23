from loguru import logger
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from .schemas import PredictionResults, InputSchema, column_map
from services.load_pipeline import load_pipeline
import sys
from uuid import uuid4
import time
import pandas as pd
# allows loading the model just once before the application starts
from contextlib import asynccontextmanager

logger.remove()  # Better observability for logs! Very important
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


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # This allows store model/pipeline inside the FastAPI app, so it can be accessible all the time
    with logger.contextualize(
        request_id="lifespan"
    ):  # I created middleware with an HTTP request to have request_id but
        logger.info(
            "Starting lifespan"
        )  # load_pipeline() and lifespan happens before application run and without any HTTP request
        try:  # so logger cannot format the logs, and we need to set them manually
            _app.state.pipeline = load_pipeline()
            yield
        finally:
            _app.state.pipeline = None
            logger.info("Ending lifespan")


app = FastAPI(lifespan=lifespan)


def get_pipeline(request: Request):
    # we create a function to return the pipeline
    pipeline = getattr(request.app.state, "pipeline", None)
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Pipeline has not beed loaded yet. Please try again later.",
        )
    # If someone calls API right after servers start and a pipeline is not yet loaded
    return pipeline


@app.middleware("http")
async def log_requests(request: Request, call_next):
    req_id = str(uuid4())
    with logger.contextualize(request_id=req_id):
        start_time = time.perf_counter()
        logger.info(f"Started {request.method} {request.url}")
        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception(
                f"Exception occurred {request.method} {request.url} - {e}"
            )
            response = JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
        elapsed_time = (time.perf_counter() - start_time) * 1000
        logger.info(
            f"⬅️ Completed {request.method} {request.url.path} "
            f"with status={getattr(response, 'status_code', 'N/A')} "
            f"in {elapsed_time:.2f}ms"
        )
        return response


@app.get("/")
async def root():
    return {
        "message": (
            "Check API endpoint `/health` to see if pipeline is "
            "loaded and ready to predictions!"
        )
    }


@app.get("/health")
async def health_check(pipeline=Depends(get_pipeline)) -> dict:
    # simple logic flor readability
    if not pipeline:
        return {"status": "No pipeline loaded yet"}
    return {"status": "Ready for predictions"}


@app.post("/predict", response_model=PredictionResults)
async def predict(
    input_data: InputSchema,
    pipeline=Depends(get_pipeline),
) -> PredictionResults:
    data_df = pd.DataFrame([input_data.model_dump()])
    data_df_mapped = data_df.rename(columns=column_map)
    try:
        pred = pipeline.predict(data_df_mapped)[0]
        prob = pipeline.predict_proba(data_df_mapped)[0, 1]
        return PredictionResults(prediction=pred, probability=prob)
    except Exception as e:
        logger.exception(f"Exception occurred while predicting values -  {e}")
        raise
