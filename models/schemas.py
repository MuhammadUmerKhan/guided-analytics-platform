from typing import List, Any
from pydantic import BaseModel, Field
from enum import StrEnum

class CanonicalColumn(StrEnum):
    TRANSACTION_ID = "transaction_id"
    ORDER_DATE = "order_date"
    CUSTOMER_ID = "customer_id"
    GENDER = "gender"
    AGE = "age"
    PRODUCT_CATEGORY = "product_category"
    QUANTITY = "quantity"
    PRICE_PER_UNIT = "price_per_unit"
    TOTAL_AMOUNT = "total_amount"

class ColumnProfile(BaseModel):
    column_name: str
    percent_missing: float = Field(..., ge=0, le=100)
    unique_count: int
    sample_values: List[Any]

class ValidationError(BaseModel):
    column: str = ""
    message: str