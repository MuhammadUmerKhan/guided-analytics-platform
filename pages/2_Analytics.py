import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from models.schemas import CanonicalColumn
from utils.ui import load_css, metric_card

st.set_page_config(page_title="Analytics Dashboard", layout="wide", page_icon="📈")
load_css()

st.title("📊 Executive Analytics Dashboard")

if "clean_df" not in st.session_state:
    st.warning("⚠️ No data available. Please upload and process data first.")
    st.page_link("pages/1_Upload_Data.py", label="Go to Upload Data", icon="📂")
    st.stop()
    
df_orig = st.session_state.clean_df.copy()

def get_col(canonical_enum: CanonicalColumn):
    return canonical_enum.value if canonical_enum.value in df_orig.columns else None

date_col = get_col(CanonicalColumn.ORDER_DATE)
total_col = get_col(CanonicalColumn.TOTAL_AMOUNT)
qty_col = get_col(CanonicalColumn.QUANTITY)
cat_col = get_col(CanonicalColumn.PRODUCT_CATEGORY)
cust_col = get_col(CanonicalColumn.CUSTOMER_ID)
price_col = get_col(CanonicalColumn.PRICE_PER_UNIT)
gender_col = get_col(CanonicalColumn.GENDER)
age_col = get_col(CanonicalColumn.AGE)

# --- Filters ---
st.sidebar.header("🎛️ Analysis Controls")
df_filtered = df_orig.copy()

if date_col:
    df_filtered[date_col] = pd.to_datetime(df_filtered[date_col], errors='coerce')
    valid_dates = df_filtered[date_col].dropna()
    if not valid_dates.empty:
        min_d, max_d = valid_dates.min().date(), valid_dates.max().date()
        if min_d != max_d:
            dr = st.sidebar.date_input("Date Range", value=(min_d, max_d), min_value=min_d, max_value=max_d)
            if len(dr) == 2:
                df_filtered = df_filtered[(df_filtered[date_col].dt.date >= dr[0]) & (df_filtered[date_col].dt.date <= dr[1])]

# --- KPIs ---
st.subheader("Business at a Glance")
k1, k2, k3, k4, k5 = st.columns(5)
# Calculations
tot_rev = df_filtered[total_col].sum() if total_col else 0
tot_ord = len(df_filtered)
avg_ord = tot_rev/tot_ord if tot_ord else 0
tot_qty = df_filtered[qty_col].sum() if qty_col else 0
uniq_cust = df_filtered[cust_col].nunique() if cust_col else 0

metric_card(k1, "Revenue", f"{tot_rev:,.0f}", "$")
metric_card(k2, "Orders", f"{tot_ord:,}")
metric_card(k3, "AOV", f"{avg_ord:,.2f}", "$")
metric_card(k4, "Units", f"{tot_qty:,}")
metric_card(k5, "Customers", f"{uniq_cust:,}")

st.markdown("---")

# --- TABS ---
tabs = st.tabs([
    "📈 Performance", 
    "📦 Products", 
    "👥 Demographics", 
    "🔬 Deep Dive",
    "📊 Distributions"
])

# 1. Performance
with tabs[0]:
    c1, c2 = st.columns([2,1])
    if date_col and total_col:
        with c1:
            st.markdown("#### Revenue Trend")
            agg = st.selectbox("Frequency", ["D", "W", "M"], index=0)
            df_ts = df_filtered.groupby(pd.Grouper(key=date_col, freq=agg))[total_col].sum().reset_index()
            fig = px.area(df_ts, x=date_col, y=total_col, template="plotly_dark", color_discrete_sequence=['#00CC96'])
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Weekly Pattern")
            df_filtered['Day'] = df_filtered[date_col].dt.day_name()
            days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            day_agg = df_filtered.groupby('Day')[total_col].sum().reindex(days).reset_index()
            fig = px.bar(day_agg, x='Day', y=total_col, template="plotly_dark", color=total_col)
            st.plotly_chart(fig, use_container_width=True)

# 2. Products
with tabs[1]:
    c1, c2 = st.columns(2)
    if cat_col and total_col:
        with c1:
            st.markdown("#### Category Share (Sunburst)")
            fig = px.sunburst(df_filtered, path=[cat_col], values=total_col, color=total_col, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.markdown("#### Top Categories (Treemap)")
            fig = px.treemap(df_filtered, path=[cat_col], values=total_col, color=total_col, template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
    if price_col and qty_col and cat_col:
        st.markdown("#### Price Elasticity (Bubble: Price vs Qty vs Revenue)")
        # Sample if too large
        plot_df = df_filtered.sample(1000) if len(df_filtered) > 1000 else df_filtered
        fig = px.scatter(plot_df, x=price_col, y=qty_col, size=total_col, color=cat_col, 
                         log_x=True, log_y=True, template="plotly_dark", title="Product Matrix")
        st.plotly_chart(fig, use_container_width=True)

# 3. Demographics (New!)
with tabs[2]:
    c1, c2 = st.columns(2)
    has_demo = False
    
    if gender_col:
        has_demo = True
        with c1:
            st.markdown("#### Gender Distribution")
            gen_count = df_filtered[gender_col].value_counts().reset_index()
            gen_count.columns = ['Gender', 'Count']
            fig = px.pie(gen_count, names='Gender', values='Count', hole=0.5, template="plotly_dark", title="Gender Split")
            st.plotly_chart(fig, use_container_width=True)
            
        if total_col:
            with c2:
                st.markdown("#### Revenue by Gender")
                gen_rev = df_filtered.groupby(gender_col)[total_col].sum().reset_index()
                fig = px.bar(gen_rev, x=gender_col, y=total_col, color=gender_col, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    if age_col:
        has_demo = True
        st.markdown("#### Age Insights")
        ac1, ac2 = st.columns(2)
        with ac1:
            fig = px.histogram(df_filtered, x=age_col, nbins=20, title="Age Histogram", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        with ac2:
            if total_col:
                fig = px.scatter(df_filtered, x=age_col, y=total_col, color=gender_col if gender_col else None,
                                 title="Age vs Spend Amount", template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

    if not has_demo:
        st.info("Map 'gender' and 'age' columns to see demographic insights.")

# 4. Deep Dive
with tabs[3]:
    c1, c2 = st.columns(2)
    if cust_col and total_col:
        with c1:
            st.markdown("#### Top Customers")
            top_c = df_filtered.groupby(cust_col)[total_col].sum().sort_values(ascending=False).head(10).reset_index()
            fig = px.bar(top_c, x=total_col, y=cust_col, orientation='h', template="plotly_dark")
            fig.update_layout(yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

    if total_col:
        with c2:
            st.markdown("#### Transaction ECDF (Cumulative)")
            fig = px.ecdf(df_filtered, x=total_col, color=gender_col if gender_col else None, template="plotly_dark", title="Spend Probability")
            st.plotly_chart(fig, use_container_width=True)
            
    # Parallel Categories
    if gender_col and cat_col:
        st.markdown("#### Customer Flow (Parallel Categories)")
        fig = px.parallel_categories(df_filtered, dimensions=[gender_col, cat_col], color=total_col if total_col else None, template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# 5. Distributions
with tabs[4]:
    st.markdown("#### Correlation Matrix")
    num_df = df_filtered.select_dtypes(include=['number'])
    if not num_df.empty:
        corr = num_df.corr()
        fig = px.imshow(corr, text_auto=True, template="plotly_dark", color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Descriptive Statistics")
    # REMOVED .style.background_gradient to fix crash
    st.dataframe(df_filtered.describe())

st.success("Analysis Updated.")
