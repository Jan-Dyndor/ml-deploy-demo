import pandas as pd
from pandas import DataFrame
from app.schemas import InputSchema, column_map
from app.main import logger


def convert_pydantic_model_to_dict(pydantic_model: InputSchema) -> dict:
    try:
        logger.debug("Started - Converting pydantic model to dict")
        result = pydantic_model.model_dump()
        logger.debug("Finished - Converting pydantic model to dict")
        return result
    except Exception as e:
        logger.exception(
            f"Exception occured while converting pydantic model to dict - {e}"
        )
        raise


def convert_dict_to_pandas_df(dict_to_convert: dict) -> pd.DataFrame:
    try:
        logger.debug("Started - Converting dict to pandas")
        result = pd.DataFrame(
            [dict_to_convert]
        )  # 1-row DataFrame with correct columns - pipleine was trained on dataframe
        logger.debug("Finished - Converting dict to pandas")
        return result
    except Exception as e:
        logger.exception(f"Exception occured while converting dict to pandas - {e}")
        raise


def map_column_names_to_pipeline_requirements(dataframe: DataFrame) -> DataFrame:
    try:
        logger.debug("Started - Mapping column names to pipeline requirements")
        result = dataframe.rename(columns=column_map)
        logger.debug("Finished - Mapping column names to pipeline requirements")
        return result
    except Exception as e:
        logger.exception(
            f"Exception occured during mapping column names to pipeline requirements - {e}"
        )
        raise

    # I created model with mean_radius but pipeline was trained on mean radius
    # it does not know what `_` is
