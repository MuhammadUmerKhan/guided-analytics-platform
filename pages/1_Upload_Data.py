import streamlit as st
import pandas as pd
from utils.profiling import profile_dataframe
from utils.mapping_rules import infer_mapping
from models.schemas import CanonicalColumn
from utils.validation import validate_mappings
from utils.canonical import create_canonical_dataset
from utils.ui import load_css

st.set_page_config(page_title="Upload & Setup", layout="wide", page_icon="📂")
load_css()

st.title("Data Upload & Setup")

# Initialize session state for mappings if not present
if "mappings" not in st.session_state:
    st.session_state.mappings = {}

# --- Step 1: Upload ---
st.subheader("1. Upload Data")
uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    # Load data only if it's a new file or not loaded yet
    if "raw_df" not in st.session_state or st.session_state.get("filename") != uploaded_file.name:
        df = pd.read_csv(uploaded_file)
        st.session_state.raw_df = df
        st.session_state.filename = uploaded_file.name
        
        # Profile data
        profiles = profile_dataframe(df)
        st.session_state.profiles = profiles
        
        # Auto-infer mappings
        inferred = infer_mapping(df.columns.tolist())
        st.session_state.mappings = inferred
        
        st.success(f"Loaded {len(df):,} rows. Columns identified.")

    # Show preview
    if "raw_df" in st.session_state:
        with st.expander("Raw Data Preview", expanded=False):
            st.dataframe(st.session_state.raw_df.head())

    # --- Step 2: Mapping ---
    st.markdown("---")
    st.subheader("2. Column Mapping")
    st.info("ℹ️ **How it works:** We try to guess your column meanings (e.g., 'Total' -> 'Total Amount'). Please verify the dropdowns below ensure detailed analysis.")
    
    st.write("Match your file's columns (left) to the standard fields (dropdown).")

    # Grid layout for mapping
    cols = st.columns(3)
    
    # We want to show a selector for each available canonical column
    # The user picks which UPLOADED column maps to it
    
    # Invert the mapping for display: Canonical -> Uploaded Col
    # (But wait, the previous logic was Uploaded -> Canonical using a dropdown per uploaded column. 
    # Let's stick to the previous pattern or improving it. 
    # The plan said: "Uses infer_mapping to pre-select dropdowns."
    # Let's iterate through the uploaded columns and show what they map to.)
    
    # Actually, it's often better to iterate through CANONICAL columns and ask "Which input column is this?", 
    # or iterate through INPUT columns and ask "What is this?".
    # Given the wide table, iterating through Input columns is safer if there are many extra columns.
    # But usually we care about filling the Canonical slots.
    
    # Let's stick to the Plan's implication: Pre-populate the mapping.
    # We will show the list of detected columns and allow mapping to Canonical.
    
    options = ['Skip'] + [field.value for field in CanonicalColumn]
    
    current_mappings = st.session_state.mappings
    
    # Create valid options that include "Skip" and the enum values
    
    updated_mappings = {}
    
    # Display in a grid
    row_cols = st.columns(3)
    
    # We iterate over the *uploaded* columns to let user decide what each one is
    # This ensures every column in the file has a chance to be mapped
    
    df_columns = st.session_state.raw_df.columns.tolist()
    
    for i, col_name in enumerate(df_columns):
        # Determine initial index for selectbox
        # Check if we have an inferred value
        default_val = 'Skip'
        if col_name in current_mappings:
             # Make sure the value is still valid
             val = current_mappings[col_name]
             if isinstance(val, CanonicalColumn):
                 val = val.value
             if val in options:
                 default_val = val
        
        try:
            idx = options.index(default_val)
        except ValueError:
            idx = 0
            
        with row_cols[i % 3]:
            selected = st.selectbox(
                f"{col_name}",
                options=options,
                index=idx,
                key=f"map_{col_name}"
            )
            
            if selected != 'Skip':
                updated_mappings[col_name] = CanonicalColumn(selected)

    # --- Step 3: Validation & Process ---
    st.markdown("---")
    col1, col2 = st.columns([1, 4])
    with col1:
        process_btn = st.button("Process Data", type="primary")
    
    if process_btn:
        errors = validate_mappings(updated_mappings)
        if errors:
            st.error("Validation Failed:")
            for e in errors:
                st.write(f"• {e.message}")
        else:
            # Perform canonical transformation
            clean_df = create_canonical_dataset(st.session_state.raw_df, updated_mappings)
            st.session_state.clean_df = clean_df
            st.session_state.final_mappings = updated_mappings
            
            st.success("Data successfully processed!")
            st.balloons()
            
            # Show link to analytics
            st.page_link("pages/2_Analytics.py", label="Go to Analytics Dashboard", icon="📊")
