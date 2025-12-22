from typing import List, Dict
from models.schemas import CanonicalColumn, ValidationError

def validate_mappings(mappings: Dict[str, CanonicalColumn]) -> List[ValidationError]:
    errors: List[ValidationError] = []

    mapped_values = list(mappings.values())
    if len(mapped_values) != len(set(mapped_values)):
        errors.append(ValidationError(message="Duplicate mapping detected. Each standard field can only be used once."))

    has_date = CanonicalColumn.ORDER_DATE in mapped_values
    has_measure = any(field in mapped_values for field in [
        CanonicalColumn.QUANTITY,
        CanonicalColumn.PRICE_PER_UNIT,
        CanonicalColumn.TOTAL_AMOUNT
    ])

    if not has_date:
        errors.append(ValidationError(message="You must map a column to 'order_date'."))
    if not has_measure:
        errors.append(ValidationError(message="You must map at least one measure: quantity, price_per_unit, or total_amount."))

    return errors