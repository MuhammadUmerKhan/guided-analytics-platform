from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# --- Data Models for Branch Analytics ---

class SalesSchema(BaseModel):
    Invoice_ID: str
    Date: datetime
    Product: str
    Category: str
    Quantity: int
    Unit_Price: int
    Branch: str
    Total_Sales: int

class ExpenseSchema(BaseModel):
    Expense_ID: str
    Date: datetime
    Expense_Type: str
    Amount: int
    Branch: str

class InventorySchema(BaseModel):
    SKU: str
    Product: str
    Stock_In: int
    Stock_Out: int
    Branch: str

class StaffSchema(BaseModel):
    Employee_ID: str
    Role: str
    Salary: int
    Branch: str

# Helper to map sheet names to schemas
SHEET_SCHEMAS = {
    'Sales': SalesSchema,
    'Expenses': ExpenseSchema,
    'Inventory': InventorySchema,
    'Staff': StaffSchema
}