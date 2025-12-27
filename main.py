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
    st.markdown("### 📂 1. Upload Data")
    st.write("""
    Securely upload your business records in Excel format. 
    Our system supports multiple sheets including **Sales**, **Expenses**, **Inventory**, and **Staff**.
    """)
    st.page_link("pages/1_Upload_Data.py", label="Get Started", icon="🚀")

with c2:
    st.markdown("### 🔍 2. Intelligent Mapping")
    st.write("""
    Forget manual data entry. Our engine automatically parses your schemas, 
    validates data types, and prepares your datasets for real-time analysis.
    """)
    
with c3:
    st.markdown("### 📊 3. Premium Analytics")
    st.write("""
    Access high-level executive summaries and deep-dive technical charts. 
    Visualize trends, monitor stock levels, and optimize staff performance instantly.
    """)
    st.page_link("pages/2_Analytics.py", label="View Analytics", icon="📈")

st.markdown("---")

# About Section
st.subheader("💡 Why Guided Analytics?")
st.write("""
This platform is engineered to transform fragmented data into a unified business command center. 
Whether you're tracking daily revenue or long-term operational costs, we provide the tools to make data-driven decisions.

**✨ Key Features:**
- 🛡️ **Deterministic Logic**: No AI hallucinations. Every number is calculated with 100% mathematical precision.
- 🎨 **Executive Aesthetics**: A clean, high-contrast dark mode designed for focus and readability.
- 📈 **Dynamic Visualizations**: interactive Plotly charts that allow you to hover, zoom, and filter by any period.
- ⚡ **Zero Setup**: Just upload your data and start analyzing immediately.
""")

st.info("👈 Use the **Sidebar** to explore your data or jump straight into the dashboard.")

