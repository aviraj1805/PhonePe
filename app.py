# app.py
# PhonePe Transaction Insights — Redesigned UI

import streamlit as st
import pandas as pd
from db_connect import get_connection
from analysis import (
    customer_segmentation, fraud_detection, geographical_insights,
    payment_performance, user_engagement, product_development,
    insurance_insights, marketing_optimization, trend_analysis,
    competitive_benchmarking
)

st.set_page_config(
    page_title="PhonePe Pulse Insights",
    layout="wide",
    page_icon="💜",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

    /* ── Root Variables ── */
    :root {
        --bg:           #F7F5FF;
        --surface:      #FFFFFF;
        --surface-2:    #F0EBF8;
        --brand:        #5B21B6;
        --brand-light:  #7C3AED;
        --brand-muted:  #EDE9FE;
        --accent:       #10B981;
        --accent-2:     #F59E0B;
        --danger:       #EF4444;
        --text-primary: #1E1B4B;
        --text-secondary: #6B7280;
        --border:       #E5E7EB;
        --radius:       12px;
        --shadow:       0 1px 3px rgba(91,33,182,0.08), 0 4px 16px rgba(91,33,182,0.06);
        --shadow-hover: 0 4px 12px rgba(91,33,182,0.15), 0 8px 32px rgba(91,33,182,0.10);
    }

    /* ── Global Reset ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: var(--text-primary);
    }

    .stApp {
        background-color: var(--bg);
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: var(--surface) !important;
        border-right: 1px solid var(--border);
        padding-top: 0 !important;
    }
    section[data-testid="stSidebar"] > div {
        padding: 0 !important;
    }

    /* ── Sidebar header band ── */
    .sidebar-header {
        background: linear-gradient(135deg, #5B21B6 0%, #7C3AED 100%);
        padding: 28px 20px 22px;
        margin-bottom: 8px;
    }
    .sidebar-header img {
        filter: brightness(0) invert(1);
    }
    .sidebar-title {
        color: rgba(255,255,255,0.95) !important;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-top: 12px;
        margin-bottom: 0;
    }

    /* ── Nav items ── */
    div[data-testid="stRadio"] label {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 20px;
        border-radius: 8px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 500;
        color: var(--text-secondary);
        transition: all 0.15s ease;
        margin: 2px 12px;
    }
    div[data-testid="stRadio"] label:hover {
        background: var(--brand-muted);
        color: var(--brand);
    }
    div[data-testid="stRadio"] label[data-baseweb="radio"] input:checked + div {
        background: var(--brand-muted);
        color: var(--brand);
    }

    /* ── Main content padding ── */
    .block-container {
        padding: 3.5rem 2.5rem 3rem !important;
        max-width: 1400px;
    }

    /* ── Page title ── */
    .page-title {
        font-size: 26px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 4px;
        letter-spacing: -0.3px;
    }
    .page-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 28px;
        font-weight: 400;
    }

    /* ── Section label ── */
    .section-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--brand-light);
        margin-bottom: 12px;
        margin-top: 32px;
    }

    /* ── Metric cards ── */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 16px;
        margin-bottom: 32px;
    }
    .kpi-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px 24px;
        box-shadow: var(--shadow);
        position: relative;
        overflow: hidden;
        transition: box-shadow 0.2s ease;
    }
    .kpi-card:hover { box-shadow: var(--shadow-hover); }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #5B21B6, #7C3AED);
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 500;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1.1;
        font-family: 'DM Mono', monospace;
    }
    .kpi-icon {
        position: absolute;
        top: 18px; right: 18px;
        font-size: 20px;
        opacity: 0.15;
    }

    /* ── Chart card wrapper ── */
    .chart-card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: var(--shadow);
    }

    /* ── Insight chips ── */
    .insight-chip {
        background: var(--surface);
        border: 1px solid var(--brand-muted);
        border-left: 3px solid var(--brand-light);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 13.5px;
        color: var(--text-primary);
        line-height: 1.5;
    }
    .insight-key {
        font-weight: 600;
        color: var(--brand);
    }

    /* ── Filter bar ── */
    .filter-bar {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 16px 20px;
        margin-bottom: 28px;
        box-shadow: var(--shadow);
    }

    /* ── Divider ── */
    .divider {
        border: none;
        border-top: 1px solid var(--border);
        margin: 28px 0;
    }

    /* ── Table ── */
    div[data-testid="stDataFrame"] {
        border-radius: var(--radius);
        overflow: hidden;
        box-shadow: var(--shadow);
    }

    /* ── Warning badge ── */
    .warn-badge {
        background: #FFF7ED;
        border: 1px solid #FED7AA;
        border-left: 3px solid var(--accent-2);
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 13px;
        color: #92400E;
        margin-bottom: 20px;
    }

    /* ── Footer ── */
    .footer {
        text-align: center;
        color: var(--text-secondary);
        font-size: 12px;
        padding: 24px 0 8px;
        border-top: 1px solid var(--border);
        margin-top: 40px;
    }

    /* ── Override Streamlit defaults ── */
    .stSelectbox label, .stRadio label {
        font-size: 13px;
        font-weight: 500;
        color: var(--text-secondary);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'DM Mono', monospace;
        font-size: 24px !important;
        color: var(--text-primary) !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 12px !important;
        color: var(--text-secondary) !important;
        font-weight: 500 !important;
    }
    .stPlotlyChart {
        border-radius: var(--radius);
    }
    /* Hide default streamlit branding */
    #MainMenu, footer[data-testid="stFooter"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────

def fetch(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def card(content_fn, *args, **kwargs):
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    content_fn(*args, **kwargs)
    st.markdown('</div>', unsafe_allow_html=True)

def section(label):
    st.markdown(f'<p class="section-label">{label}</p>', unsafe_allow_html=True)

def footer():
    st.markdown(
        '<div class="footer">Data Source: PhonePe Pulse GitHub &nbsp;·&nbsp; Built with Streamlit</div>',
        unsafe_allow_html=True
    )


# ── Sidebar ──────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        <div style="display:flex; align-items:center; gap:10px;">
            <div style="background:white; border-radius:8px; width:36px; height:36px;
                        display:flex; align-items:center; justify-content:center;
                        font-size:20px; font-weight:800; color:#5B21B6;">P</div>
            <div>
                <div style="color:white; font-size:15px; font-weight:700; letter-spacing:0.02em;">PhonePe</div>
                <div style="color:rgba(255,255,255,0.7); font-size:10px; font-weight:500; letter-spacing:0.12em; text-transform:uppercase;">Pulse Insights</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='padding: 0 12px;'>", unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["Overview", "Transaction Analysis", "User Analysis", "Insurance Analysis", "Fraud & Risk Detection"],
        label_visibility="collapsed"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-top:1px solid #E5E7EB; margin: 16px 12px;'>", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:11px; color:#9CA3AF; padding: 0 20px; line-height:1.5;'>"
        "Real-time analytics on PhonePe transaction data across India."
        "</p>",
        unsafe_allow_html=True
    )


# ── PAGE 1: OVERVIEW ─────────────────────────────────────────────

if page == "Overview":
    st.markdown('<p class="page-title">PhonePe Pulse — Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">High-level performance metrics and platform insights</p>', unsafe_allow_html=True)

    # KPI Row
    total_txn   = fetch("SELECT SUM(transaction_count) AS val FROM aggregated_transaction")["val"][0]
    total_amt   = fetch("SELECT SUM(transaction_amount) AS val FROM aggregated_transaction")["val"][0]
    total_users = fetch("SELECT SUM(registered_users) AS val FROM aggregated_user")["val"][0]

    st.markdown("""
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-label">Total Transactions</div>
            <div class="kpi-value">{:,}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon">₹</div>
            <div class="kpi-label">Total Volume</div>
            <div class="kpi-value">₹{:,.0f}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-icon"></div>
            <div class="kpi-label">Registered Users</div>
            <div class="kpi-value">{:,}</div>
        </div>
    </div>
    """.format(int(total_txn), float(total_amt), int(total_users)), unsafe_allow_html=True)

    # Charts
    section("PLATFORM SNAPSHOT")
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(payment_performance(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(product_development(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Insights
    section("KEY INSIGHTS")
    from insights import generate_insights
    insights = generate_insights()
    keys = list(insights.keys())
    col1, col2 = st.columns(2, gap="large")
    for i, key in enumerate(keys):
        chip = f"""<div class="insight-chip">
            <span class="insight-key">{key.replace('_', ' ').title()}</span><br>
            {insights[key]}
        </div>"""
        if i % 2 == 0:
            col1.markdown(chip, unsafe_allow_html=True)
        else:
            col2.markdown(chip, unsafe_allow_html=True)

    footer()


# ── PAGE 2: TRANSACTION ANALYSIS ─────────────────────────────────

elif page == "Transaction Analysis":
    st.markdown('<p class="page-title">Transaction Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Explore payment trends, categories, and regional performance</p>', unsafe_allow_html=True)

    # Filter bar
    years    = fetch("SELECT DISTINCT year FROM aggregated_transaction ORDER BY year")["year"].tolist()
    quarters = [1, 2, 3, 4]
    states   = fetch("SELECT DISTINCT state FROM aggregated_transaction ORDER BY state")["state"].tolist()

    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    sel_year    = col1.selectbox("Year",    ["All"] + [str(y) for y in years])
    sel_quarter = col2.selectbox("Quarter", ["All"] + [str(q) for q in quarters])
    sel_state   = col3.selectbox("State",   ["All"] + states)
    st.markdown('</div>', unsafe_allow_html=True)

    def build_filter():
        conds = []
        if sel_year    != "All": conds.append(f"year = {sel_year}")
        if sel_quarter != "All": conds.append(f"quarter = {sel_quarter}")
        if sel_state   != "All": conds.append(f"state = '{sel_state}'")
        return " WHERE " + " AND ".join(conds) if conds else ""

    w = build_filter()

    import plotly.express as px

    section("TRANSACTION AMOUNT BY STATE — TOP 20")
    col_geo1, col_geo2 = st.columns([2, 1], gap="large")

    with col_geo1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(geographical_insights(), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_geo2:
        # Top 5 states summary table
        df_top5 = fetch("""
            SELECT state, ROUND(SUM(transaction_amount)/1e9, 2) AS amount_bn,
                   SUM(transaction_count) AS txn_count
            FROM aggregated_transaction
            GROUP BY state ORDER BY amount_bn DESC LIMIT 5
        """)
        df_top5["state"] = df_top5["state"].str.replace("-", " ").str.title()
        df_top5.columns = ["State", "Amount (₹B)", "Transactions"]

        st.markdown("""
        <div style="background:var(--surface); border:1px solid var(--border);
                    border-radius:var(--radius); padding:20px; box-shadow:var(--shadow); height:100%;">
            <p style="font-size:11px; font-weight:600; letter-spacing:0.1em;
                      text-transform:uppercase; color:var(--brand-light); margin-bottom:14px;">
                TOP 5 STATES
            </p>
        """, unsafe_allow_html=True)

        for i, row in df_top5.iterrows():
            rank_color = ["#5B21B6","#7C3AED","#A78BFA","#C4B5FD","#DDD6FE"][i]
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:12px;
                        padding:10px 0; border-bottom:1px solid var(--border);">
                <div style="background:{rank_color}; color:white; font-size:11px;
                            font-weight:700; border-radius:50%; width:24px; height:24px;
                            display:flex; align-items:center; justify-content:center;
                            flex-shrink:0;">{i+1}</div>
                <div style="flex:1; min-width:0;">
                    <div style="font-size:13px; font-weight:600; color:var(--text-primary);
                                white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                        {row['State']}
                    </div>
                    <div style="font-size:11px; color:var(--text-secondary);">
                        ₹{row['Amount (₹B)']}B &nbsp;·&nbsp; {int(row['Transactions']):,} txns
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        section("PAYMENT CATEGORIES")
        df_pay = fetch(f"""
            SELECT transaction_type,
                   SUM(transaction_count) AS total_count,
                   ROUND(SUM(transaction_amount),2) AS total_amount
            FROM aggregated_transaction{w}
            GROUP BY transaction_type
            ORDER BY total_count DESC
        """)
        fig_pay = px.pie(
            df_pay, names="transaction_type", values="total_count",
            title="Payment Type Breakdown",
            color_discrete_sequence=["#5B21B6","#7C3AED","#A78BFA","#C4B5FD","#DDD6FE","#10B981"]
        )
        fig_pay.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_family="DM Sans", title_font_size=14,
            legend=dict(font_size=12)
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_pay, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        section("QUARTERLY TRENDS")
        df_qtr = fetch(f"""
            SELECT year, quarter,
                   SUM(transaction_count) AS total_count,
                   ROUND(SUM(transaction_amount),2) AS total_amount
            FROM aggregated_transaction{w}
            GROUP BY year, quarter
            ORDER BY year, quarter
        """)
        df_qtr["quarter_label"] = "Q" + df_qtr["quarter"].astype(str) + " " + df_qtr["year"].astype(str)
        fig_qtr = px.bar(
            df_qtr, x="quarter_label", y="total_count", color="total_amount",
            title="Quarterly Transaction Volume",
            labels={"quarter_label": "Quarter", "total_count": "Transactions"},
            color_continuous_scale=["#EDE9FE","#7C3AED","#5B21B6"]
        )
        fig_qtr.update_xaxes(tickangle=45)
        fig_qtr.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_family="DM Sans", title_font_size=14
        )
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig_qtr, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    section("VOLUME TREND BY PAYMENT TYPE")
    df_trend = fetch(f"""
        SELECT year, quarter, transaction_type,
               SUM(transaction_count) AS total_count,
               ROUND(SUM(transaction_amount),2) AS total_amount
        FROM aggregated_transaction{w}
        GROUP BY year, quarter, transaction_type
        ORDER BY year, quarter, total_count DESC
    """)
    df_trend["quarter_label"] = "Q" + df_trend["quarter"].astype(str) + " " + df_trend["year"].astype(str)
    fig_trend = px.line(
        df_trend, x="quarter_label", y="total_count", color="transaction_type", markers=True,
        title="Transaction Volume Trend by Type",
        labels={"quarter_label": "Quarter", "total_count": "Transactions"},
        color_discrete_sequence=["#5B21B6","#7C3AED","#10B981","#F59E0B","#EF4444","#6B7280"]
    )
    fig_trend.update_xaxes(tickangle=45)
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", title_font_size=14
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    section("COMPETITIVE BENCHMARKING — TOP 10")
    figs = competitive_benchmarking()
    for fig in figs:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    footer()


# ── PAGE 3: USER ANALYSIS ────────────────────────────────────────

elif page == "User Analysis":
    st.markdown('<p class="page-title">User Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Registered user base, growth trends, and market opportunity</p>', unsafe_allow_html=True)

    years  = fetch("SELECT DISTINCT year FROM aggregated_user ORDER BY year")["year"].tolist()
    states = fetch("SELECT DISTINCT state FROM aggregated_user ORDER BY state")["state"].tolist()

    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    sel_year  = col1.selectbox("Year",  ["All"] + [str(y) for y in years])
    sel_state = col2.selectbox("State", ["All"] + states)
    st.markdown('</div>', unsafe_allow_html=True)

    def user_filter():
        conds = []
        if sel_year  != "All": conds.append(f"year = {sel_year}")
        if sel_state != "All": conds.append(f"state = '{sel_state}'")
        return " WHERE " + " AND ".join(conds) if conds else ""

    w = user_filter()
    import plotly.express as px

    section("CUSTOMER SEGMENTATION")
    df_seg = fetch(f"""
        SELECT state, SUM(registered_users) AS total_users
        FROM aggregated_user{w}
        GROUP BY state ORDER BY total_users DESC LIMIT 10
    """)
    df_seg["state"] = df_seg["state"].str.replace("-", " ").str.title()
    fig_seg = px.bar(
        df_seg, x="total_users", y="state", orientation="h",
        title="Top 10 States by Registered Users",
        labels={"total_users": "Total Users", "state": "State"},
        color="total_users",
        color_continuous_scale=["#EDE9FE","#7C3AED","#5B21B6"]
    )
    fig_seg.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", title_font_size=14, yaxis=dict(autorange="reversed")
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_seg, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="insight-chip">Maharashtra and Uttar Pradesh consistently lead in registered users across all periods.</div>',
        unsafe_allow_html=True
    )

    section("YEAR-OVER-YEAR USER GROWTH")
    df_yoy = fetch(f"""
        SELECT state, year, SUM(registered_users) AS total_users
        FROM aggregated_user{w}
        GROUP BY state, year ORDER BY state, year
    """)
    df_yoy["state"] = df_yoy["state"].str.replace("-", " ").str.title()
    top_states = df_yoy.groupby("state")["total_users"].sum().nlargest(7).index.tolist()
    df_yoy = df_yoy[df_yoy["state"].isin(top_states)]
    fig_yoy = px.line(
        df_yoy, x="year", y="total_users", color="state", markers=True,
        title="YoY User Growth — Top 7 States",
        labels={"total_users": "Total Users", "year": "Year"},
        color_discrete_sequence=["#5B21B6","#7C3AED","#10B981","#F59E0B","#EF4444","#6B7280","#A78BFA"]
    )
    fig_yoy.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", title_font_size=14
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_yoy, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="insight-chip">User growth peaked in 2021 across most states, coinciding with pandemic-driven digital adoption.</div>',
        unsafe_allow_html=True
    )

    section("MARKETING OPTIMIZATION — UNTAPPED MARKETS")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(marketing_optimization(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="insight-chip">States with high user counts but low transaction amounts represent strong growth opportunities for targeted campaigns.</div>',
        unsafe_allow_html=True
    )

    footer()


# ── PAGE 4: INSURANCE ANALYSIS ───────────────────────────────────

elif page == "Insurance Analysis":
    st.markdown('<p class="page-title">Insurance Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Policy distribution and premium volumes across states</p>', unsafe_allow_html=True)

    years  = fetch("SELECT DISTINCT year FROM aggregated_insurance ORDER BY year")["year"].tolist()
    states = fetch("SELECT DISTINCT state FROM aggregated_insurance ORDER BY state")["state"].tolist()

    st.markdown('<div class="filter-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    sel_year  = col1.selectbox("Year",  ["All"] + [str(y) for y in years])
    sel_state = col2.selectbox("State", ["All"] + states)
    st.markdown('</div>', unsafe_allow_html=True)

    def ins_filter():
        conds = []
        if sel_year  != "All": conds.append(f"year = {sel_year}")
        if sel_state != "All": conds.append(f"state = '{sel_state}'")
        return " WHERE " + " AND ".join(conds) if conds else ""

    w = ins_filter()
    import plotly.express as px

    df_ins = fetch(f"""
        SELECT state,
               SUM(insurance_count) AS total_policies,
               ROUND(SUM(insurance_amount),2) AS total_amount
        FROM aggregated_insurance{w}
        GROUP BY state ORDER BY total_policies DESC LIMIT 10
    """)
    df_ins["state"] = df_ins["state"].str.replace("-", " ").str.title()

    section("POLICY DISTRIBUTION BY STATE")
    fig_ins = px.bar(
        df_ins, x="state", y="total_policies", color="total_amount",
        title="Top 10 States by Insurance Policies",
        labels={"state": "State", "total_policies": "Total Policies", "total_amount": "Total Premium (₹)"},
        color_continuous_scale=["#FFF7ED","#F59E0B","#D97706"]
    )
    fig_ins.update_xaxes(tickangle=45)
    fig_ins.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans", title_font_size=14
    )
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_ins, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    section("DATA TABLE")
    st.dataframe(df_ins, use_container_width=True, hide_index=True)

    footer()


# ── PAGE 5: FRAUD & RISK DETECTION ───────────────────────────────

elif page == "Fraud & Risk Detection":
    st.markdown('<p class="page-title">Fraud & Risk Detection</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-subtitle">Pattern-based anomaly detection across transaction data</p>', unsafe_allow_html=True)

    st.markdown(
        '<div class="warn-badge"><strong>Disclaimer:</strong> This is statistical pattern analysis only — not confirmed fraud detection. '
        'High transaction count with low average amount may indicate micro-transactions, not fraudulent activity.</div>',
        unsafe_allow_html=True
    )

    section("ANOMALY SCATTER — VOLUME VS. AVG TRANSACTION SIZE")
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fraud_detection(), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    section("TOP 10 FLAGGED STATES — HIGH VOLUME, LOW AVG AMOUNT")
    df_fraud = fetch("""
        SELECT state,
               SUM(transaction_count) AS total_count,
               ROUND(SUM(transaction_amount),2) AS total_amount,
               ROUND(SUM(transaction_amount)/SUM(transaction_count),2) AS avg_amount_per_txn
        FROM aggregated_transaction
        GROUP BY state
        ORDER BY total_count DESC, avg_amount_per_txn ASC
        LIMIT 10
    """)
    df_fraud["state"] = df_fraud["state"].str.replace("-", " ").str.title()
    st.dataframe(df_fraud, use_container_width=True, hide_index=True)

    footer()