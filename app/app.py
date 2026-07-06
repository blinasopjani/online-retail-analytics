"""
Phase 3 — Streamlit Application (Dev C).

Steps 3.1 + 3.2:
  - CSV upload + auto-cleaning via clean_data()
  - Column format validation with clear error messages
  - Full interactive dashboard (KPIs, charts, recommendations)
  - What-if module placeholder (Step 5.1)
  - Export button placeholder (Step 5.2)
"""

import sys
import os
import io
import pandas as pd
import streamlit as st

# ── Path setup ─────────────────────────────────────────────────────────
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_cleaning import clean_data
from analysis import (
    get_kpi_summary, get_monthly_revenue, get_revenue_by_hour,
    get_revenue_by_day_of_week, get_top_products, get_worst_products,
    get_product_return_rate, get_country_performance,
    get_customer_lifetime_value, get_new_vs_returning_customers,
    get_churned_customers, get_return_summary,
)
from recommendation_engine import compute_rfm, get_segment_summary, generate_recommendations
from visualisations import (
    plot_monthly_revenue, plot_revenue_by_hour, plot_revenue_by_day_of_week,
    plot_top_products, plot_product_return_rates,
    plot_rfm_segments, plot_segment_revenue_share, plot_clv_distribution,
    plot_new_vs_returning, plot_country_revenue, plot_top_countries_bar,
    format_kpi_cards,
)

# ── Required columns for validation ───────────────────────────────────
# Raw format uses 'Price' and 'Customer ID'; cleaned export uses 'UnitPrice' and 'CustomerID'
REQUIRED_COLUMNS = {'Invoice', 'StockCode', 'Description',
                    'Quantity', 'InvoiceDate', 'Country'}
# These columns have accepted aliases (raw name → cleaned name)
COLUMN_ALIASES = {
    'Price':       'UnitPrice',
    'Customer ID': 'CustomerID',
}

# ── Page config ────────────────────────────────────────────────────────
st.set_page_config(
    page_title='Retail Analytics Platform',
    page_icon='📊',
    layout='wide',
    initial_sidebar_state='expanded',
)

# ── Inject custom CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0F1117;
    color: #EAEAEA;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1A1D2E 0%, #0F1117 100%);
    border-right: 1px solid #2A2D3E;
}
[data-testid="stSidebar"] .block-container { padding-top: 2rem; }

/* Metric cards */
[data-testid="metric-container"] {
    background: linear-gradient(135deg, #1E2130 0%, #252840 100%);
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    transition: transform 0.2s ease;
}
[data-testid="metric-container"]:hover { transform: translateY(-2px); }
[data-testid="stMetricValue"]  { color: #6C63FF !important; font-size: 1.8rem !important; }
[data-testid="stMetricLabel"]  { color: #8D99AE !important; font-size: 0.85rem !important; }

/* Section headers */
h2 { color: #6C63FF; border-bottom: 1px solid #2A2D3E; padding-bottom: 0.4rem; }
h3 { color: #EAEAEA; }

/* Upload area */
[data-testid="stFileUploader"] {
    background: #1E2130;
    border: 2px dashed #6C63FF;
    border-radius: 12px;
    padding: 1rem;
}

/* Info / warning / success boxes */
.stAlert { border-radius: 10px; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] { background: #1E2130; border-radius: 10px; }
.stTabs [data-baseweb="tab"]      { color: #8D99AE; }
.stTabs [aria-selected="true"]    { color: #6C63FF !important; font-weight: 600; }

/* Recommendation cards */
.rec-card {
    background: linear-gradient(135deg, #1E2130 0%, #252840 100%);
    border-left: 4px solid #6C63FF;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.rec-card.high   { border-left-color: #E71D36; }
.rec-card.medium { border-left-color: #F7931E; }
.rec-card.low    { border-left-color: #2EC4B6; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 📊 Retail Analytics")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        ["🏠 Home & Upload", "📈 Dashboard", "👥 Customer Analysis",
         "🌍 Geographic", "🔁 Recommendations", "🔮 What-If Simulator"],
        label_visibility='collapsed',
    )

    st.markdown("---")
    st.caption("Online Retail Analytics Platform")


# ══════════════════════════════════════════════════════════════════════
# SESSION STATE — shared cleaned df across pages
# ══════════════════════════════════════════════════════════════════════

if 'df_clean' not in st.session_state:
    st.session_state['df_clean'] = None
if 'filename' not in st.session_state:
    st.session_state['filename'] = None


# ══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════

def validate_columns(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """Check if uploaded file has the required columns.

    Accepts both raw format (Price, Customer ID) and pre-cleaned format
    (UnitPrice, CustomerID) so users can upload either version.
    """
    cols = set(df.columns)
    missing = []
    for req in REQUIRED_COLUMNS:
        alias = COLUMN_ALIASES.get(req)          # e.g. 'Price' → 'UnitPrice'
        rev_alias = {v: k for k, v in COLUMN_ALIASES.items()}.get(req)  # reverse
        if req not in cols and (alias not in cols) and (rev_alias not in cols):
            missing.append(req)
    # Check price column (Price OR UnitPrice)
    if 'Price' not in cols and 'UnitPrice' not in cols:
        missing.append('Price / UnitPrice')
    # Check customer column (Customer ID OR CustomerID)
    if 'Customer ID' not in cols and 'CustomerID' not in cols:
        missing.append('Customer ID / CustomerID')
    return len(missing) == 0, missing


def is_already_cleaned(df: pd.DataFrame) -> bool:
    """Return True if the CSV is already in the cleaned format (has Revenue & CustomerID)."""
    return 'Revenue' in df.columns and 'CustomerID' in df.columns and 'IsReturn' in df.columns


def load_and_clean(uploaded_file) -> pd.DataFrame | None:
    """Read CSV, rename columns if needed, then run clean_data() — or skip
    cleaning if the file is already in the cleaned format.
    """
    try:
        df_raw = pd.read_csv(uploaded_file, parse_dates=['InvoiceDate'])
    except Exception as e:
        st.error(f"❌ Could not read file: {e}")
        return None

    ok, missing = validate_columns(df_raw)
    if not ok:
        st.error(
            f"❌ **Invalid file format.** Missing required columns: `{', '.join(missing)}`\n\n"
            "Expected columns: `Invoice, StockCode, Description, Quantity, "
            "InvoiceDate, Price (or UnitPrice), Customer ID (or CustomerID), Country`"
        )
        return None

    # If the file is already cleaned (e.g. cleaned_retail_data.csv), skip re-cleaning
    if is_already_cleaned(df_raw):
        return df_raw

    # Raw file — rename Price → UnitPrice then run cleaner
    if 'Price' in df_raw.columns and 'UnitPrice' not in df_raw.columns:
        df_raw = df_raw.rename(columns={'Price': 'UnitPrice'})

    with st.spinner("🧹 Cleaning data..."):
        df_clean = clean_data(df_raw)

    return df_clean


def require_data() -> bool:
    """Show a prompt if no data is loaded yet. Returns True if data is ready."""
    if st.session_state['df_clean'] is None:
        st.info("📂 Please upload a CSV file on the **🏠 Home & Upload** page first.")
        return False
    return True


# ══════════════════════════════════════════════════════════════════════
# PAGE: HOME & UPLOAD
# ══════════════════════════════════════════════════════════════════════

if page == "🏠 Home & Upload":
    st.title("📊 Online Retail Analytics Platform")
    st.markdown(
        "Upload your monthly sales CSV and the platform will automatically "
        "clean, analyse, and generate business recommendations."
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### Upload Monthly Sales Data")
        uploaded = st.file_uploader(
            "Drop your CSV here (Online Retail II format)",
            type=["csv"],
            key="uploader",
        )

        st.markdown("— **OR** —")

        if st.button("Load local default dataset (`data/cleaned_retail_data.csv`)"):
            import os
            default_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cleaned_retail_data.csv')
            if os.path.exists(default_path):
                with st.spinner("Loading local file..."):
                    df = pd.read_csv(default_path, parse_dates=['InvoiceDate'])
                    st.session_state['df_clean'] = df
                    st.session_state['filename'] = 'cleaned_retail_data.csv'
                st.success("✅ Local default dataset loaded successfully!")
            else:
                st.error("❌ `cleaned_retail_data.csv` not found in `data/`. Please run `01_data_exploration.ipynb` first.")

        if uploaded:
            df = load_and_clean(uploaded)
            if df is not None:
                st.session_state['df_clean'] = df
                st.session_state['filename'] = uploaded.name
                st.success(
                    f"✅ **{uploaded.name}** loaded successfully — "
                    f"**{len(df):,}** rows after cleaning."
                )

    with col2:
        st.markdown("### Expected Format")
        st.markdown("""
| Column | Type |
|--------|------|
| `Invoice` | string |
| `StockCode` | string |
| `Description` | string |
| `Quantity` | integer |
| `InvoiceDate` | datetime |
| `Price` | float |
| `Customer ID` | float/str |
| `Country` | string |
        """)

    # Show currently loaded file
    if st.session_state['df_clean'] is not None:
        st.markdown("---")
        st.markdown(f"### 📁 Currently loaded: `{st.session_state['filename']}`")
        df = st.session_state['df_clean']
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Rows (after cleaning)", f"{len(df):,}")
        c2.metric("Columns", str(df.shape[1]))
        c3.metric("Date range",
                  f"{pd.to_datetime(df['InvoiceDate']).min().strftime('%b %Y')}"
                  f" → {pd.to_datetime(df['InvoiceDate']).max().strftime('%b %Y')}"
                  if 'InvoiceDate' in df.columns else 'N/A')
        c4.metric("Countries", str(df['Country'].nunique()) if 'Country' in df.columns else 'N/A')

        with st.expander("Preview first 50 rows"):
            st.dataframe(df.head(50), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: DASHBOARD
# ══════════════════════════════════════════════════════════════════════

elif page == "📈 Dashboard":
    st.title("📈 Sales Dashboard")
    if not require_data():
        st.stop()

    df = st.session_state['df_clean']

    # ── KPIs ────────────────────────────────────────────────────────
    kpis = get_kpi_summary(df)
    cards = format_kpi_cards(kpis)

    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        col.metric(card['label'], card['value'])

    st.markdown("---")

    # ── Tabs ────────────────────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📅 Revenue Trends", "📦 Products", "📊 Returns"])

    with tab1:
        monthly = get_monthly_revenue(df)
        st.plotly_chart(plot_monthly_revenue(monthly), use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            dow = get_revenue_by_day_of_week(df)
            st.plotly_chart(plot_revenue_by_day_of_week(dow), use_container_width=True)
        with c2:
            hourly = get_revenue_by_hour(df)
            st.plotly_chart(plot_revenue_by_hour(hourly), use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            top_n = st.slider("Top N products", 5, 20, 10, key="top_n")
            top = get_top_products(df, n=top_n)
            st.plotly_chart(plot_top_products(top, n=top_n), use_container_width=True)
        with c2:
            worst = get_worst_products(df, n=10)
            st.plotly_chart(plot_top_products(worst, n=10), use_container_width=True)
            st.caption("⬆ Worst-selling products — consider repricing or discontinuation")

    with tab3:
        ret_summary = get_return_summary(df)
        if ret_summary:
            rc1, rc2, rc3 = st.columns(3)
            rc1.metric("Return Transactions", f"{ret_summary.get('return_transactions', 0):,}")
            rc2.metric("Return Rate", f"{ret_summary.get('return_rate_%', 0):.1f}%")
            rc3.metric("Revenue Lost to Returns",
                       f"£{ret_summary.get('revenue_lost_from_returns', 0):,.0f}")

        ret_rate = get_product_return_rate(df)
        st.plotly_chart(plot_product_return_rates(ret_rate, n=15), use_container_width=True)


# ══════════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER ANALYSIS
# ══════════════════════════════════════════════════════════════════════

elif page == "👥 Customer Analysis":
    st.title("👥 Customer Analysis")
    if not require_data():
        st.stop()

    df = st.session_state['df_clean']

    with st.spinner("Computing RFM scores..."):
        rfm = compute_rfm(df)
        seg_summary = get_segment_summary(rfm)

    # Segment overview
    st.markdown("### Customer Segments")
    c1, c2 = st.columns(2)
    with c1:
        st.plotly_chart(plot_rfm_segments(seg_summary), use_container_width=True)
    with c2:
        st.plotly_chart(plot_segment_revenue_share(seg_summary), use_container_width=True)

    st.dataframe(seg_summary.style.format({
        'Avg_Recency_Days': '{:.0f}',
        'Avg_Frequency':    '{:.1f}',
        'Avg_Revenue':      '£{:,.0f}',
        'Total_Revenue':    '£{:,.0f}',
    }), use_container_width=True)

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["💰 CLV", "🔄 New vs Returning", "⚠️ Churn Risk"])

    with tab1:
        clv = get_customer_lifetime_value(df)
        st.plotly_chart(plot_clv_distribution(clv), use_container_width=True)
        if not clv.empty:
            top10_pct = clv.head(max(1, int(len(clv) * 0.1)))
            rev_share = top10_pct['TotalRevenue'].sum() / clv['TotalRevenue'].sum() * 100
            st.info(f"🏆 Top 10% of customers generate **{rev_share:.1f}%** of total revenue")
        with st.expander("Full CLV table"):
            st.dataframe(clv.head(100), use_container_width=True)

    with tab2:
        new_ret = get_new_vs_returning_customers(df)
        st.plotly_chart(plot_new_vs_returning(new_ret), use_container_width=True)

    with tab3:
        days = st.slider("Inactive for more than (days)", 30, 180, 90, step=15)
        churned = get_churned_customers(df, days_threshold=days)
        st.metric(f"Customers inactive {days}+ days", f"{len(churned):,}")
        if not churned.empty:
            st.dataframe(churned.head(50), use_container_width=True)
            csv_export = churned.to_csv(index=False).encode()
            st.download_button(
                "⬇ Download churn list (CSV)",
                data=csv_export,
                file_name=f"churn_risk_{days}days.csv",
                mime="text/csv",
            )


# ══════════════════════════════════════════════════════════════════════
# PAGE: GEOGRAPHIC
# ══════════════════════════════════════════════════════════════════════

elif page == "🌍 Geographic":
    st.title("🌍 Geographic Performance")
    if not require_data():
        st.stop()

    df = st.session_state['df_clean']
    geo = get_country_performance(df)

    exclude_uk = st.toggle("Exclude United Kingdom (avoids scale distortion)", value=True)

    st.plotly_chart(plot_country_revenue(geo, exclude_uk=exclude_uk), use_container_width=True)

    c1, c2 = st.columns([2, 1])
    with c1:
        n = st.slider("Top N countries", 5, 20, 10, key="geo_n")
        st.plotly_chart(plot_top_countries_bar(geo, n=n, exclude_uk=exclude_uk),
                        use_container_width=True)
    with c2:
        st.markdown("### Country Table")
        display_geo = geo[geo['Country'] != 'United Kingdom'] if exclude_uk else geo
        st.dataframe(
            display_geo.head(20).style.format({'Revenue': '£{:,.0f}'}),
            use_container_width=True,
        )


# ══════════════════════════════════════════════════════════════════════
# PAGE: RECOMMENDATIONS
# ══════════════════════════════════════════════════════════════════════

elif page == "🔁 Recommendations":
    st.title("🔁 Business Recommendations")
    if not require_data():
        st.stop()

    df = st.session_state['df_clean']

    with st.spinner("Generating recommendations..."):
        recs = generate_recommendations(df)

    if not recs:
        st.warning("Not enough data to generate recommendations.")
        st.stop()

    # Summary counts
    high   = [r for r in recs if r['priority'] == 'High']
    medium = [r for r in recs if r['priority'] == 'Medium']
    low    = [r for r in recs if r['priority'] == 'Low']

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Recommendations", str(len(recs)))
    c2.metric("🔴 High Priority", str(len(high)))
    c3.metric("🟠 Medium Priority", str(len(medium)))
    c4.metric("🟢 Low Priority", str(len(low)))

    st.markdown("---")

    priority_filter = st.multiselect(
        "Filter by priority", ["High", "Medium", "Low"],
        default=["High", "Medium", "Low"],
    )

    for rec in recs:
        if rec['priority'] not in priority_filter:
            continue

        css_class = rec['priority'].lower()
        priority_emoji = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}[rec['priority']]

        st.markdown(f"""
<div class="rec-card {css_class}">
  <strong>{priority_emoji} {rec['title']}</strong>
  &nbsp;&nbsp;<span style="color:#8D99AE; font-size:0.85rem">{rec['type']} · {rec['segment']}</span><br><br>
  {rec['message']}<br><br>
  <span style="color:#6C63FF; font-weight:600">📈 Estimated impact: ~+{rec['impact_pct']}% profit improvement</span>
</div>
""", unsafe_allow_html=True)

    # Export recommendations as CSV
    st.markdown("---")
    rec_df = pd.DataFrame(recs)
    st.download_button(
        "⬇ Export Recommendations (CSV)",
        data=rec_df.to_csv(index=False).encode(),
        file_name="recommendations.csv",
        mime="text/csv",
    )


# ══════════════════════════════════════════════════════════════════════
# PAGE: WHAT-IF SIMULATOR (Step 5.1 placeholder)
# ══════════════════════════════════════════════════════════════════════

elif page == "🔮 What-If Simulator":
    st.title("🔮 What-If Profit Simulator")
    if not require_data():
        st.stop()

    df = st.session_state['df_clean']
    kpis = get_kpi_summary(df)
    base_revenue = kpis.get('total_revenue', 0)

    st.markdown(
        "Adjust the sliders below to simulate the revenue impact of business actions. "
        "*(Logic will be fully implemented in Step 5.1)*"
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📊 Your Assumptions")
        vip_retention = st.slider(
            "🏆 Improve VIP customer retention by", 0, 30, 10, step=1,
            format="%d%%", help="% increase in repeat purchases from Champion segment"
        )
        winback_rate = st.slider(
            "🔄 Win back At-Risk customers", 0, 50, 20, step=5,
            format="%d%%", help="% of at-risk customers you re-engage"
        )
        return_reduction = st.slider(
            "📦 Reduce product returns by", 0, 50, 15, step=5,
            format="%d%%", help="% reduction in return transaction losses"
        )
        new_customer_growth = st.slider(
            "🆕 Increase new customer acquisition", 0, 30, 5, step=1,
            format="%d%%", help="% more new customers per month"
        )

    with col2:
        st.markdown("#### 💡 Projected Impact")

        # Simple projection formulas (Dev B will implement full logic in Step 5.1)
        ret_summary = get_return_summary(df)
        revenue_from_vip    = base_revenue * (vip_retention / 100) * 0.30  # champions ~30%
        revenue_from_winback = base_revenue * (winback_rate / 100) * 0.10
        revenue_from_returns = ret_summary.get('revenue_lost_from_returns', 0) * (return_reduction / 100)
        revenue_from_new    = base_revenue * (new_customer_growth / 100) * 0.05
        total_uplift        = revenue_from_vip + revenue_from_winback + revenue_from_returns + revenue_from_new

        st.metric("Base Revenue", f"£{base_revenue:,.0f}")
        st.metric("VIP Retention Uplift", f"+£{revenue_from_vip:,.0f}")
        st.metric("Win-Back Revenue", f"+£{revenue_from_winback:,.0f}")
        st.metric("Returns Savings", f"+£{revenue_from_returns:,.0f}")
        st.metric("New Customer Revenue", f"+£{revenue_from_new:,.0f}")
        st.markdown("---")
        st.metric("🎯 Projected Total Revenue",
                  f"£{base_revenue + total_uplift:,.0f}",
                  delta=f"+£{total_uplift:,.0f} (+{total_uplift/base_revenue*100:.1f}%)"
                  if base_revenue > 0 else None)

    st.caption(
        "⚠️ These are simplified estimates. Step 5.1 will connect these to the full "
        "RFM history and `kpi_history` MongoDB collection for accurate projections."
    )
