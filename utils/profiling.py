import pandas as pd
from typing import List
from models.schemas import ColumnProfile
from config import settings

def profile_dataframe(df: pd.DataFrame) -> List[ColumnProfile]:
    if len(df) < settings.min_row_count:
        raise ValueError(f"Dataset must have at least {settings.min_row_count} rows.")

    profiles = []
    for col in df.columns:
        series = df[col]
        percent_missing = (series.isnull().sum() / len(series)) * 100
        unique_count = series.nunique()
        sample_values = series.dropna().head(5).tolist()

        profiles.append(ColumnProfile(
            column_name=col,
            percent_missing=round(percent_missing, 2),
            unique_count=unique_count,
            sample_values=sample_values
        ))
    return profiles