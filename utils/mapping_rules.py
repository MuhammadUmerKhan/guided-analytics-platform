from typing import List, Dict, Optional
from models.schemas import CanonicalColumn

# Define heuristics for each canonical column
# The keys correspond to the CanonicalColumn values
MAPPING_RULES = {
    CanonicalColumn.TRANSACTION_ID: ["id", "trans", "txn", "transaction", "invoice", "receipt"],
    CanonicalColumn.ORDER_DATE: ["date", "time", "ordered_at", "created_at", "timestamp", "day"],
    CanonicalColumn.CUSTOMER_ID: ["cust", "customer", "member", "client"],
    CanonicalColumn.GENDER: ["gender", "sex"],
    CanonicalColumn.AGE: ["age", "birth", "dob", "year_of_birth"],
    CanonicalColumn.PRODUCT_CATEGORY: ["category", "cat", "product_type", "department", "segment"],
    CanonicalColumn.QUANTITY: ["qty", "quantity", "count", "units", "items"],
    CanonicalColumn.PRICE_PER_UNIT: ["price", "unit_price", "cost", "rate", "amount_per_unit"],
    CanonicalColumn.TOTAL_AMOUNT: ["total", "amount", "revenue", "sales", "grand_total"]
}

def normalize_column_name(col_name: str) -> str:
    """Normalizes a column name for easier matching."""
    return col_name.lower().strip().replace(" ", "_").replace("-", "_")

def infer_mapping(columns: List[str]) -> Dict[str, CanonicalColumn]:
    """
    Infers the mapping of uploaded columns to canonical columns based on rules.
    Returns a dictionary where keys are uploaded column names and values are CanonicalColumns.
    """
    mapping = {}
    used_canonical = set()

    # Pre-calculate normalized uploaded columns
    normalized_cols = {col: normalize_column_name(col) for col in columns}

    # Iterate through potential canonical fields
    # We prioritize finding a match for each canonical field
    for canonical_field, keywords in MAPPING_RULES.items():
        if canonical_field in used_canonical:
            continue
            
        best_match = None
        
        # Check against all uploaded columns
        for original_col, norm_col in normalized_cols.items():
            # Skip if this column is already mapped
            if original_col in mapping:
                continue
                
            # Exact match check
            if norm_col == canonical_field.value:
                best_match = original_col
                break
            
            # Keyword match check
            for keyword in keywords:
                # We look for the keyword as a substring or exact match
                # Use word boundaries or strict containment
                if keyword in norm_col:
                     # Simple heuristic: pick the first one matching a keyword
                     # A more complex one might score similarity
                     best_match = original_col
                     break
            
            if best_match:
                break
        
        if best_match:
            mapping[best_match] = canonical_field
            used_canonical.add(canonical_field)
            
    return mapping
