import streamlit as st
from utils.ui import load_css

st.set_page_config(page_title="Guided Analytics", layout="wide", page_icon="🚀")

# Inject Global CSS
load_css()

# Hero Section
st.markdown("""
<div style="text-align: center; padding: 40px 0;">
    <h1 style="font-size: 3.5rem; margin-bottom: 10px;">Guided Analytics Platform</h1>
    <p style="font-size: 1.2rem; color: #babcbf;">Transform your raw CSV data into actionable business intelligence in minutes.</p>
</div>
""", unsafe_allow_html=True)

# Main Content Grid
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 1. Upload Data")
    st.write("Simply drag & drop your CSV file. We support flexible schemas including transactions, sales, and customer data.")
    st.page_link("pages/1_Upload_Data.py", label="Start Upload", icon="📂")

with c2:
    st.markdown("### 2. Auto-Mapping")
    st.write("Our intelligent rule-engine automatically detects your columns (Dates, Revenue, Quantity) so you don't have to.")
    
with c3:
    st.markdown("### 3. Executive Insights")
    st.write("Unlock immediate value with a premium dashboard featuring Time Series, Cohort Analysis, and Segmentation.")
    st.page_link("pages/2_Analytics.py", label="View Dashboard", icon="📊")

st.markdown("---")

# About Section
st.subheader("💡 About This Project")
st.write("""
This platform is designed to eliminate the repetitive work of building one-off dashboards. 
Review your **Sales Performance**, understand **Customer Demographics**, and optimize your **Product Strategy** all in one place.

**Key Features:**
- 🛡️ **No AI Hallucinations**: Deterministic, rule-based logic ensures 100% accuracy.
- 🎨 **Premium UI**: Designed for executives with clean, dark-mode aesthetics.
- ✨ **Interactive Charts**: Drill down into data with Plotly-powered visualizations.
""")

st.info("👈 Use the **Sidebar** to navigate between steps.")
