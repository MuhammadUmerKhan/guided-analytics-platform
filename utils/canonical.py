import pandas as pd
import streamlit as st
from typing import Dict
from models.schemas import CanonicalColumn

def create_canonical_dataset(df: pd.DataFrame, mappings: Dict[str, CanonicalColumn]) -> pd.DataFrame:
    # Rename selected columns to canonical names
    rename_map = {uploaded: can.value for uploaded, can in mappings.items()}
    clean_df = df[list(mappings.keys())].rename(columns=rename_map).copy()

    # Force data types based on canonical rules
    if 'order_date' in clean_df.columns:
        clean_df['order_date'] = pd.to_datetime(clean_df['order_date'], errors='coerce', dayfirst=True)

    numeric_fields = ['quantity', 'price_per_unit', 'total_amount', 'age']
    for col in numeric_fields:
        if col in clean_df.columns:
            clean_df[col] = pd.to_numeric(clean_df[col], errors='coerce')

    # Drop rows with critical failures
    critical_cols = ['order_date']
    if 'total_amount' in clean_df.columns:
        critical_cols.append('total_amount')

    initial_rows = len(clean_df)
    clean_df = clean_df.dropna(subset=critical_cols)
    dropped = initial_rows - len(clean_df)

    if dropped > 0:
        st.warning(f"Dropped {dropped} rows due to invalid/missing data in key columns after casting.")

    return clean_df