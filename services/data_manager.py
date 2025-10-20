import pandas as pd
from pandas import DataFrame
from app.schemas import InputSchema, column_map


def convert_pydantic_model_to_dict(pydantic_model:InputSchema) -> dict:
    return pydantic_model.model_dump()

def convert_dict_to_pandas_df(dict_to_convert : dict) -> pd.DataFrame:
    return pd.DataFrame([dict_to_convert]) # 1-row DataFrame with correct columns - pipleine was trained on dataframe

def map_column_names_to_pipeline_requrements(dataframe: DataFrame) -> DataFrame:
    return dataframe.rename(columns=column_map, inplace=True)
    # I created model with mean_radius but pipeline was trained on mean radius
    # it does not know what `_` is



