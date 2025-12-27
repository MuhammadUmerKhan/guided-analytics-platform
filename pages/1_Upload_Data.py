import streamlit as st
import pandas as pd
import os
from utils.ui import load_css
from models.schemas import SHEET_SCHEMAS

st.set_page_config(page_title="Data Setup", layout="wide", page_icon="📂")
load_css()

st.title("📂 Data Setup & Onboarding")
st.markdown("""
Welcome to the setup phase. Follow these **three simple steps** to prepare your branch data for analysis.
""")

if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

# --- Step 1: Upload ---
st.subheader("1️⃣ Step 1: Upload Your Data")
with st.expander("📄 View Requirements & Template Info", expanded=False):
    st.write("""
    Your Excel file should contain the following **4 sheets**:
    - **Sales**: Transactional data (Invoice ID, Product, Total_Sales, etc.)
    - **Expenses**: Cost records (Expense Type, Amount, etc.)
    - **Inventory**: Stock levels (SKU, Stock In, Stock Out)
    - **Staff**: Employee details (Role, Salary)
    """)

uploaded_file = st.file_uploader("Choose an Excel file (.xlsx)", type=["xlsx"], help="Upload the master branch data file here.")

if uploaded_file is not None:
    # --- Step 2: Process ---
    st.subheader("2️⃣ Step 2: Validate & Process")
    if st.button("🚀 Process Uploaded Data", type="primary"):
        try:
            xl = pd.ExcelFile(uploaded_file)
            required_sheets = ['Sales', 'Expenses', 'Inventory', 'Staff']
            
            # Verify sheets
            if not all(sheet in xl.sheet_names for sheet in required_sheets):
                st.error(f"❌ Missing required sheets in uploaded file. Found: {xl.sheet_names}")
                st.stop()
                
            # Load DataFrames
            dfs = {}
            with st.status("🔍 Validating schemas and loading records...", expanded=True) as status:
                for sheet in required_sheets:
                    st.write(f"📥 Loading {sheet}...")
                    df = pd.read_excel(uploaded_file, sheet_name=sheet)
                    
                    # Validation logic (Schema Check)
                    schema_model = SHEET_SCHEMAS[sheet]
                    try:
                        required_cols = schema_model.model_fields.keys()
                    except AttributeError:
                        required_cols = schema_model.__fields__.keys()
                        
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    
                    if missing_cols:
                        st.error(f"❌ {sheet}: Missing columns {missing_cols}")
                        status.update(label="Validation Failed", state="error")
                        st.stop()
                    
                    dfs[sheet] = df
                    st.write(f"✅ {sheet}: Validated {len(df)} records")
                    
                status.update(label="✨ Data successfully loaded!", state="complete", expanded=False)
                
            st.session_state.dfs = dfs
            st.session_state.data_loaded = True
            
        except Exception as e:
            st.error(f"🚨 Failed to process uploaded file: {str(e)}")

# --- Step 3: Preview & Navigate ---
if st.session_state.data_loaded:
    st.subheader("3️⃣ Step 3: Preview & Analysis")
    st.success("✅ Your data is ready for analysis!")
    
    # Data Preview
    with st.expander("👀 Data Preview (First 5 Rows)", expanded=False):
        required_sheets = ['Sales', 'Expenses', 'Inventory', 'Staff']
        tabs = st.tabs([f"📄 {s}" for s in required_sheets])
        
        for i, sheet in enumerate(required_sheets):
            with tabs[i]:
                if "dfs" in st.session_state and sheet in st.session_state.dfs:
                    df_preview = st.session_state.dfs[sheet]
                    st.dataframe(df_preview.head(), width='stretch')
                    st.caption(f"💡 {len(df_preview)} records found in {sheet}")
            
    st.markdown("---")
    st.page_link("pages/2_Analytics.py", label="📊 Go to Analytics Dashboard", icon="📈")
else:
    st.info("💡 Please upload an Excel file in Step 1 to begin.")

