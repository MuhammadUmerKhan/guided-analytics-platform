import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ui import load_css, metric_card

st.set_page_config(page_title="Branch Analytics", layout="wide", page_icon="📈")
load_css()

# --- Helper Functions ---
def filter_by_date(df, date_col):
    if df is None or date_col not in df.columns:
        return df
    
    df[date_col] = pd.to_datetime(df[date_col])
    min_date = df[date_col].min().date()
    max_date = df[date_col].max().date()
    
    if pd.isnull(min_date) or pd.isnull(max_date) or min_date == max_date:
        return df

    st.sidebar.subheader("📅 Global Date Filter")
    date_range = st.sidebar.date_input(
        "Select Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="global_date_filter"
    )
    
    if len(date_range) == 2:
        mask = (df[date_col].dt.date >= date_range[0]) & (df[date_col].dt.date <= date_range[1])
        return df[mask]
    return df

# --- Main App ---
st.title("📈 Branch Analytics Command Center")
st.markdown("""
Welcome to your executive dashboard. Monitor key performance indicators, 
track operational efficiency, and drill down into branch-specific data.
""")

if "dfs" not in st.session_state or "data_loaded" not in st.session_state or not st.session_state.data_loaded:
    st.warning("⚠️ No data loaded. Please go to the Data Setup page to upload your file.")
    st.page_link("pages/1_Upload_Data.py", label="Go to Data Setup", icon="📂")
    st.stop()

# Retrieve DataFrames
df_sales = st.session_state.dfs['Sales'].copy()
df_expenses = st.session_state.dfs['Expenses'].copy()
df_inventory = st.session_state.dfs['Inventory'].copy()
df_staff = st.session_state.dfs['Staff'].copy()

# Apply Global Filter
df_sales_filtered = filter_by_date(df_sales, 'Date')

# Sync Expense Filter
if 'global_date_filter' in st.session_state and len(st.session_state.global_date_filter) == 2:
    start_d, end_d = st.session_state.global_date_filter
    df_expenses['Date'] = pd.to_datetime(df_expenses['Date'])
    mask_exp = (df_expenses['Date'].dt.date >= start_d) & (df_expenses['Date'].dt.date <= end_d)
    df_expenses_filtered = df_expenses[mask_exp]
else:
    df_expenses_filtered = df_expenses

# --- Tabs ---
tabs = st.tabs([
    "🏠 Overview", 
    "🛍️ Sales Analysis", 
    "💸 Expense Analysis", 
    "📦 Inventory", 
    "👥 Staff"
])

# ==========================================
# 1. OVERVIEW
# ==========================================
with tabs[0]:
    st.markdown("### 🏢 Executive Summary")
    st.write("A high-level view of your branch's financial and operational health.")
    
    # Kpi Calculations
    total_sales = df_sales_filtered['Total_Sales'].sum()
    total_expenses = df_expenses_filtered['Amount'].sum()
    net_profit = total_sales - total_expenses
    profit_margin = (net_profit / total_sales * 100) if total_sales > 0 else 0
    total_orders = len(df_sales_filtered)
    
    # KPIS
    k1, k2, k3, k4 = st.columns(4)
    metric_card(k1, "Total Sales", f"${total_sales:,.0f}", "Gross Revenue")
    metric_card(k2, "Total Expenses", f"${total_expenses:,.0f}", "Operational Costs")
    metric_card(k3, "Net Profit", f"${net_profit:,.0f}", f"Margin: {profit_margin:.1f}%")
    metric_card(k4, "Total Orders", f"{total_orders:,}", "Transactions handled")
    
    st.markdown("---")
    
    # Chart 1: Sales vs Expenses Trend
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown("#### 📉 Revenue & Cost Dynamics")
        st.caption("How your daily revenue tracks against operational expenditures.")
        sales_ts = df_sales_filtered.groupby(pd.Grouper(key='Date', freq='D'))['Total_Sales'].sum().reset_index()
        exp_ts = df_expenses_filtered.groupby(pd.Grouper(key='Date', freq='D'))['Amount'].sum().reset_index()
        
        fig_ts = go.Figure()
        fig_ts.add_trace(go.Scatter(x=sales_ts['Date'], y=sales_ts['Total_Sales'], mode='lines', name='Sales', line=dict(color='#00CC96', width=3)))
        fig_ts.add_trace(go.Scatter(x=exp_ts['Date'], y=exp_ts['Amount'], mode='lines', name='Expenses', line=dict(color='#EF553B', width=3)))
        fig_ts.update_layout(template="plotly_dark", hovermode="x unified", legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_ts, width='stretch')

    with c2:
        st.markdown("#### 🌊 Profit Waterfall")
        st.caption("Visualizing the bridge from Revenue to Net Profit.")
        fig_water = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Sales", "Expenses", "Net Profit"],
            y = [total_sales, -total_expenses, net_profit],
            connector = {"line":{"color":"gray"}},
            text = [f"${total_sales/1000:.1f}k", f"-${total_expenses/1000:.1f}k", f"${net_profit/1000:.1f}k"],
            textposition = "auto"
        ))
        fig_water.update_layout(template="plotly_dark", showlegend=False)
        st.plotly_chart(fig_water, width='stretch')

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("#### 🏆 Top Sales Categories")
        st.caption("identifying which product groups drive the most revenue.")
        top_cat = df_sales_filtered.groupby('Category')['Total_Sales'].sum().reset_index().sort_values('Total_Sales', ascending=False)
        fig_cat = px.bar(top_cat, x='Category', y='Total_Sales', color='Total_Sales', template="plotly_dark", color_continuous_scale='Teal')
        st.plotly_chart(fig_cat, width='stretch')

    with c4:
        st.markdown("#### 💸 Expense Allocation")
        st.caption("Top 5 cost centers contributing to total expenses.")
        top_exp = df_expenses_filtered.groupby('Expense_Type')['Amount'].sum().reset_index().sort_values('Amount', ascending=False).head(5)
        fig_exp = px.bar(top_exp, x='Amount', y='Expense_Type', orientation='h', template="plotly_dark", color='Amount', color_continuous_scale='Reds')
        st.plotly_chart(fig_exp, width='stretch')

# ==========================================
# 2. SALES ANALYSIS
# ==========================================
with tabs[1]:
    st.markdown("### 🛍️ Sales Deep Dive")
    st.write("Detailed breakdown of sales patterns, product performance, and customer trends.")
    
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("#### 🎯 Market Share by Category")
        st.caption("Percentage distribution of gross sales across product categories.")
        fig_pie = px.pie(df_sales_filtered, names='Category', values='Total_Sales', hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_pie, width='stretch')

    with r1c2:
        st.markdown("#### 🔝 Top 10 High-Performance Products")
        st.caption("Products generating the highest total sales volume.")
        top_prod = df_sales_filtered.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_bar = px.bar(top_prod, x='Total_Sales', y='Product', orientation='h', template="plotly_dark", color='Total_Sales', color_continuous_scale='Viridis')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, width='stretch')
        
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown("#### 📅 Category Heatmap (Day of Week)")
        st.caption("Multivariate: Identifying peak shopping days for each category.")
        df_sales_filtered['Day'] = df_sales_filtered['Date'].dt.day_name()
        days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data = df_sales_filtered.pivot_table(index='Category', columns='Day', values='Total_Sales', aggfunc='sum').reindex(columns=days_order)
        fig_heat = px.imshow(heatmap_data, labels=dict(x="Day", y="Category", color="Sales"), template="plotly_dark", color_continuous_scale='GnBu')
        st.plotly_chart(fig_heat, width='stretch')

    with r2c2:
        st.markdown("#### 📈 Average Order Value (AOV) Trend")
        st.caption("Bivariate: Tracking the average spend per transaction over time.")
        aov_ts = df_sales_filtered.groupby(pd.Grouper(key='Date', freq='D')).apply(lambda x: x['Total_Sales'].sum() / len(x) if len(x) > 0 else 0).reset_index()
        aov_ts.columns = ['Date', 'AOV']
        fig_aov = px.line(aov_ts, x='Date', y='AOV', template="plotly_dark", line_shape='spline', render_mode='svg')
        fig_aov.update_traces(line=dict(color='#AB63FA', width=3))
        st.plotly_chart(fig_aov, width='stretch')
        
    r3c1, r3c2 = st.columns(2)
    with r3c1:
        st.markdown("#### 📅 Weekly Sales Patterns (Restored)")
        st.caption("Univariate: Average daily sales volume across the week.")
        daily_perf = df_sales_filtered.groupby('Day')['Total_Sales'].mean().reindex(days_order).reset_index()
        fig_day = px.bar(daily_perf, x='Day', y='Total_Sales', template="plotly_dark", color='Total_Sales', color_continuous_scale='Purples')
        st.plotly_chart(fig_day, width='stretch')

    with r3c2:
        st.markdown("#### 🗓️ Monthly Revenue Trend")
        st.caption("Bivariate: Long-term revenue trajectory grouped by month.")
        monthly_sales = df_sales_filtered.groupby(pd.Grouper(key='Date', freq='ME'))['Total_Sales'].sum().reset_index()
        fig_month = px.line(monthly_sales, x='Date', y='Total_Sales', template="plotly_dark", markers=True)
        st.plotly_chart(fig_month, width='stretch')

    r4c1, r4c2 = st.columns(2)
    with r4c1:
        st.markdown("#### 📦 Category Volatility")
        st.caption("Bivariate: Distribution of order values within each category.")
        fig_box_cat = px.box(df_sales_filtered, x='Category', y='Total_Sales', color='Category', template="plotly_dark")
        st.plotly_chart(fig_box_cat, width='stretch')

    with r4c2:
        st.markdown("#### ⛰️ Cumulative Revenue Growth")
        st.caption("Bivariate: Accumulated revenue over the selected period.")
        df_sorted = df_sales_filtered.sort_values('Date')
        df_sorted['Cumulative'] = df_sorted['Total_Sales'].cumsum()
        fig_cum = px.area(df_sorted, x='Date', y='Cumulative', template="plotly_dark", color_discrete_sequence=['#00CC96'])
        st.plotly_chart(fig_cum, width='stretch')

# ==========================================
# 3. EXPENSE ANALYSIS
# ==========================================
with tabs[2]:
    st.markdown("### 💸 Cost Center Analysis")
    st.write("Explore where the branch's money is being spent.")
    
    e1, e2 = st.columns(2)
    with e1:
        st.markdown("#### 🗺️ Expense Hierarchy")
        st.caption("Multivariate: Treemap visualization of categorical spending.")
        fig_etree = px.treemap(df_expenses_filtered, path=['Expense_Type'], values='Amount', color='Amount', template="plotly_dark", color_continuous_scale='magma')
        st.plotly_chart(fig_etree, width='stretch')
        
    with e2:
        st.markdown("#### 📉 Daily Expense Volatility (Restored)")
        st.caption("Bivariate: Tracking daily spending across expense types.")
        fig_eline = px.line(df_expenses_filtered, x='Date', y='Amount', color='Expense_Type', template="plotly_dark")
        st.plotly_chart(fig_eline, width='stretch')
        
    e3, e4 = st.columns(2)
    with e3:
        st.markdown("#### 🥧 Expense Frequency (Restored)")
        st.caption("Univariate: Most common types of expenditure transactions.")
        exp_counts = df_expenses_filtered['Expense_Type'].value_counts().reset_index()
        exp_counts.columns = ['Type', 'Count']
        fig_ecount = px.pie(exp_counts, names='Type', values='Count', template="plotly_dark", hole=0.3)
        st.plotly_chart(fig_ecount, width='stretch')

    with e4:
        st.markdown("#### 📊 Efficiency: Sales to Expense Ratio")
        st.caption("Bivariate: Revenue efficiency tracking. Target > 1.0.")
        d_sales = df_sales_filtered.groupby(pd.Grouper(key='Date', freq='D'))['Total_Sales'].sum()
        d_exp = df_expenses_filtered.groupby(pd.Grouper(key='Date', freq='D'))['Amount'].sum()
        ratio_df = (d_sales / d_exp.replace(0, 1)).reset_index()
        ratio_df.columns = ['Date', 'Ratio']
        fig_ratio = px.bar(ratio_df, x='Date', y='Ratio', template="plotly_dark", color='Ratio', color_continuous_scale='RdYlGn')
        fig_ratio.add_hline(y=1, line_dash="dash", line_color="white")
        st.plotly_chart(fig_ratio, width='stretch')
        
    e5, e6 = st.columns(2)
    with e5:
        st.markdown("#### ⛰️ Cumulative Expenses (Restored)")
        st.caption("Bivariate: Accumulated operational costs over time.")
        df_exp_sort = df_expenses_filtered.sort_values('Date')
        df_exp_sort['Cum_Exp'] = df_exp_sort['Amount'].cumsum()
        fig_ecum = px.area(df_exp_sort, x='Date', y='Cum_Exp', template="plotly_dark", color_discrete_sequence=['#EF553B'])
        st.plotly_chart(fig_ecum, width='stretch')

    with e6:
        st.markdown("#### 📋 Latest Expenditure Ledger")
        st.caption("Historical log of recent transactions.")
        st.dataframe(df_expenses_filtered.sort_values('Date', ascending=False).head(100), width='stretch')

# ==========================================
# 4. INVENTORY
# ==========================================
with tabs[3]:
    st.markdown("### 📦 Inventory & Logistics")
    st.write("Monitor stock movement, turnover rates, and inventory health.")
    
    i1, i2 = st.columns(2)
    with i1:
        st.markdown("#### 🔄 Stock Flow Matrix")
        st.caption("Bivariate: Comparing Stock In vs Stock Out volumes.")
        stock_agg = df_inventory.melt(id_vars=['Product', 'SKU'], value_vars=['Stock_In', 'Stock_Out'], var_name='Type', value_name='Count')
        fig_stock = px.bar(stock_agg, x='Product', y='Count', color='Type', barmode='group', template="plotly_dark")
        st.plotly_chart(fig_stock, width='stretch')

    with i2:
        st.markdown("#### ⚡ Stock Velocity Index")
        st.caption("Multivariate: Analyzing movement speed vs. replenishment volume.")
        df_inventory['Velocity'] = df_inventory['Stock_Out'] / (df_inventory['Stock_In'] + df_inventory['Stock_Out']).replace(0, 1)
        fig_vel = px.scatter(df_inventory, x='Stock_In', y='Stock_Out', size='Velocity', color='Velocity', hover_name='Product', template="plotly_dark")
        st.plotly_chart(fig_vel, width='stretch')

    i3, i4 = st.columns(2)
    with i3:
        st.markdown("#### 🔥 Top Demand Items (Restored)")
        st.caption("Univariate: Highest turnover items by stock-out count.")
        top_out = df_inventory.sort_values('Stock_Out', ascending=False).head(10)
        fig_out = px.bar(top_out, x='Stock_Out', y='Product', orientation='h', template="plotly_dark", color='Stock_Out', color_continuous_scale='Oranges')
        st.plotly_chart(fig_out, width='stretch')

    with i4:
        st.markdown("#### 🏗️ Top Restocked Items (Restored)")
        st.caption("Univariate: Most frequent replenishment candidates.")
        top_in = df_inventory.sort_values('Stock_In', ascending=False).head(10)
        fig_in = px.bar(top_in, x='Stock_In', y='Product', orientation='h', template="plotly_dark", color='Stock_In', color_continuous_scale='Blues')
        st.plotly_chart(fig_in, width='stretch')

    i5, i6 = st.columns(2)
    with i5:
        st.markdown("#### 🩺 Inventory Health (Ratio)")
        st.caption("Univariate: Ratio distribution of outflow to inflow.")
        df_inventory['Ratio'] = df_inventory['Stock_Out'] / df_inventory['Stock_In'].replace(0, 1)
        fig_hist_inv = px.histogram(df_inventory, x='Ratio', nbins=20, template="plotly_dark")
        st.plotly_chart(fig_hist_inv, width='stretch')

    with i6:
        st.markdown("#### 🗺️ Correlation: Inbound vs Outbound")
        st.caption("Bivariate: Regression view of replenishment vs consumption.")
        fig_corr = px.scatter(df_inventory, x='Stock_In', y='Stock_Out', trendline="ols", template="plotly_dark", color_discrete_sequence=['#FF6692'])
        st.plotly_chart(fig_corr, width='stretch')

# ==========================================
# 5. STAFF
# ==========================================
with tabs[4]:
    st.markdown("### 👥 HR & Operational Efficiency")
    st.write("Analyze workforce allocation and productivity metrics.")
    
    s1, s2 = st.columns(2)
    with s1:
        st.markdown("#### 🧩 Role Distribution")
        st.caption("Univariate: Staff count breakdown.")
        role_counts = df_staff['Role'].value_counts().reset_index()
        role_counts.columns = ['Role', 'Count']
        fig_role = px.pie(role_counts, names='Role', values='Count', hole=0.5, template="plotly_dark")
        st.plotly_chart(fig_role, width='stretch')

    with s2:
        st.markdown("#### 💰 ROI: Revenue vs Salary Efficiency")
        st.caption("Bivariate: Revenue generated per dollar of salary spend.")
        total_rev = df_sales_filtered['Total_Sales'].sum()
        role_rev_efficiency = df_staff.groupby('Role')['Salary'].sum().reset_index()
        role_rev_efficiency['Efficiency'] = total_rev / role_rev_efficiency['Salary']
        fig_eff = px.bar(role_rev_efficiency, x='Role', y='Efficiency', template="plotly_dark", color='Efficiency', color_continuous_scale='Greens')
        st.plotly_chart(fig_eff, width='stretch')

    s3, s4 = st.columns(2)
    with s3:
        st.markdown("#### 💵 Salary Cost per Role (Restored)")
        st.caption("Univariate: Total payroll expenditure by job category.")
        role_sal = df_staff.groupby('Role')['Salary'].sum().reset_index()
        fig_sal_bar = px.bar(role_sal, x='Role', y='Salary', template="plotly_dark", color='Salary')
        st.plotly_chart(fig_sal_bar, width='stretch')

    with s4:
        st.markdown("#### 📏 Salary Benchmarking (Box Plot)")
        st.caption("Bivariate: Compensation ranges across roles.")
        fig_box = px.box(df_staff, x='Role', y='Salary', color='Role', template="plotly_dark")
        st.plotly_chart(fig_box, width='stretch')

    s5, s6 = st.columns(2)
    with s5:
        st.markdown("#### 📊 Salary Histogram (Restored)")
        st.caption("Univariate: Distribution of salary brackets across the branch.")
        fig_hist_sal = px.histogram(df_staff, x='Salary', nbins=15, template="plotly_dark")
        st.plotly_chart(fig_hist_sal, width='stretch')

    with s6:
        st.markdown("#### 📋 Staff Directory")
        st.dataframe(df_staff[['Employee_ID', 'Role', 'Salary']], width='stretch')

st.success("✅ Dashboard expanded with 20+ comprehensive visualizations.")
