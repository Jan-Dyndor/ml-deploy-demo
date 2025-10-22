from loguru import logger
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from .schemas import PredictionResults, InputSchema
from services.load_pipeline import load_pipeline
import sys
from uuid import uuid4
import time
from services.data_manager import (
    convert_pydantic_model_to_dict,
    convert_dict_to_pandas_df,
    map_column_names_to_pipeline_requirements,
)
from contextlib import (
    asynccontextmanager,
)  # allows to load model just once befre application starts

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
async def lifespan(
    app: FastAPI,
):  # This allows to stroe model/pipeline inside FastAPI app sso it can be accesible all time
    with logger.contextualize(
        request_id="lifespan"
    ):  # I created middleware with HTTP requeest to have request_id but
        logger.info(
            "Starting lifespan"
        )  # load_pipeline() and lifespan happens befre application run and without any HTTP request
        try:  # sologger can not foramt the logs and we need to set them manually
            app.state.pipeline = load_pipeline()
            yield
        finally:
            app.state.pipeline = None
            logger.info("Ending lifespan")


app = FastAPI(lifespan=lifespan)


def get_pipeline(request: Request):  # we create function to return the pipleine
    pipeline = getattr(request.app.state, "pipeline", None)
    if pipeline is None:
        raise HTTPException(
            status_code=503,
            detail="Pipeline has not beed loaded yet. Please try again later.",
        )
    # Is someone will call API right after servers start and pipeline is not yet loaded
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
            logger.exception(f"Exception occurred {request.method} {request.url} - {e}")
            response = JSONResponse(
                status_code=500, content={"detail": "Internal Server Error"}
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
    return {"message": "Check API endpoint `/health` to see if pipeline is loaded and redy to predictions!"}

@app.get("/health")
async def health_check(pipeline = Depends(get_pipeline)) -> dict:
    if pipeline:
        return {"status": "Ready for predictions"}
    else:
        return {"status": "No pipeline loaded yet"}


@app.post("/predict", response_model=PredictionResults)
async def predict(
    input_data: InputSchema, pipeline=Depends(get_pipeline)
) -> PredictionResults:
    input_dict = convert_pydantic_model_to_dict(input_data)
    data_df = convert_dict_to_pandas_df(
        input_dict
    )  # 1-row DataFrame with correct columns - pipleine was trained on dataframe
    data_df_mapped = map_column_names_to_pipeline_requirements(data_df)
    try:
        pred = pipeline.predict(data_df_mapped)[0]
        proba = pipeline.predict_proba(data_df_mapped)[0, 1]
        return PredictionResults(prediction=pred, probability=proba)
    except Exception as e:
        logger.exception(f"Exception occurred while predicting values -  {e}")
        raise
