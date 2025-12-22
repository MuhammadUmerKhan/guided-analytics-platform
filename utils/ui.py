import streamlit as st

def load_css():
    """Injects global CSS for a consistent, premium look."""
    st.markdown("""
        <style>
            /* Main Background & Text */
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            
            /* Sidebar */
            [data-testid="stSidebar"] {
                background-color: #262730;
                border-right: 1px solid #464b5c;
            }
            
            /* Metric Cards */
            .metric-card {
                background-color: #1e212b; /* Slightly lighter than bg */
                border: 1px solid #464b5c;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.3);
                text-align: center;
                transition: transform 0.2s;
            }
            .metric-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0,0,0,0.5);
                border-color: #00ADB5; /* Teal accent */
            }
            .metric-title {
                color: #A0A0A0;
                font-size: 0.85rem;
                text-transform: uppercase;
                letter-spacing: 1px;
                margin-bottom: 8px;
            }
            .metric-value {
                color: #FFFFFF;
                font-size: 1.8rem;
                font-weight: 700;
            }
            
            /* Headers */
            h1, h2, h3 {
                font-family: 'Inter', sans-serif;
                font-weight: 600;
                color: #f0f2f6;
            }
            h1 {
                background: -webkit-linear-gradient(45deg, #00ADB5, #EEEEEE);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            
            /* Buttons */
            .stButton>button {
                border-radius: 6px;
                font-weight: 600;
            }
            
            /* Plotly Charts */
            .stPlotlyChart {
                background-color: #1e212b;
                border-radius: 8px;
                padding: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.2);
            }
        </style>
    """, unsafe_allow_html=True)

def project_header():
    """Renders a consistent header across pages."""
    st.markdown("# 🚀 Guided Analytics Platform")
    st.markdown("---")

def metric_card(col, title, value, prefix="", suffix=""):
    """Renders a styled metric card."""
    col.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{title}</div>
        <div class="metric-value">{prefix}{value}{suffix}</div>
    </div>
    """, unsafe_allow_html=True)
