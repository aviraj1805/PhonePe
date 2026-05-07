# analysis.py
# Contains 10 chart-generation functions using Plotly, fetched from phonepe_pulse database.

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from db_connect import get_connection
from queries import QUERIES
import os

CHARTS_DIR = "charts"
os.makedirs(CHARTS_DIR, exist_ok=True)

def fetch(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def customer_segmentation():
    df = fetch(QUERIES["customer_segmentation"])
    df["state"] = df["state"].str.replace("-", " ").str.title()
    fig = px.bar(df, x="total_users", y="state", orientation="h",
                 title="Top 10 States by Registered Users",
                 labels={"total_users": "Total Users", "state": "State"},
                 color="total_users", color_continuous_scale="Blues")
    fig.write_html(f"{CHARTS_DIR}/customer_segmentation.html")
    return fig

def fraud_detection():
    df = fetch(QUERIES["fraud_detection"])
    df["state"] = df["state"].str.replace("-", " ").str.title()
    fig = px.scatter(df, x="total_count", y="avg_amount_per_txn", text="state",
                     title="Fraud Detection: Transaction Count vs Avg Amount per Transaction",
                     labels={"total_count": "Total Transaction Count", "avg_amount_per_txn": "Avg Amount per Txn (₹)"},
                     color="avg_amount_per_txn", color_continuous_scale="Reds", size="total_count")
    fig.update_traces(textposition="top center")
    fig.write_html(f"{CHARTS_DIR}/fraud_detection.html")
    return fig

def geographical_insights():
    df = fetch(QUERIES["geographical_insights"])
    df["state"] = df["state"].str.replace("-", " ").str.title()
    
    # Use a simple bar chart — reliable, no external GeoJSON dependency
    df_sorted = df.sort_values("total_amount", ascending=False).head(20)
    fig = px.bar(
        df_sorted, x="state", y="total_amount",
        title="Transaction Amount by State",
        labels={"state": "State", "total_amount": "Total Amount (₹)"},
        color="total_amount",
        color_continuous_scale=["#EDE9FE", "#7C3AED", "#5B21B6"]
    )
    fig.update_xaxes(tickangle=45)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans",
        title_font_size=14,
        showlegend=False
    )
    fig.write_html(f"{CHARTS_DIR}/geographical_insights.html")
    return fig

def payment_performance():
    df = fetch(QUERIES["payment_performance"])
    fig = px.pie(df, names="transaction_type", values="total_count",
                 title="Payment Performance: Transaction Share by Type",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.write_html(f"{CHARTS_DIR}/payment_performance.html")
    return fig

def user_engagement():
    df = fetch(QUERIES["user_engagement"])
    df["state"] = df["state"].str.replace("-", " ").str.title()
    top_states = df.groupby("state")["total_users"].sum().nlargest(7).index.tolist()
    df = df[df["state"].isin(top_states)]
    fig = px.line(df, x="year", y="total_users", color="state", markers=True,
                  title="User Engagement: Year-over-Year User Growth by State",
                  labels={"total_users": "Total Users", "year": "Year", "state": "State"})
    fig.write_html(f"{CHARTS_DIR}/user_engagement.html")
    return fig

def product_development():
    df = fetch(QUERIES["product_development"])
    df["quarter_label"] = "Q" + df["quarter"].astype(str) + " " + df["year"].astype(str)
    fig = px.bar(df, x="quarter_label", y="total_count", color="total_amount",
                 title="Product Development: Quarter-wise Transaction Trends",
                 labels={"quarter_label": "Quarter", "total_count": "Total Transactions", "total_amount": "Total Amount (₹)"},
                 color_continuous_scale="Teal")
    fig.update_xaxes(tickangle=45)
    fig.write_html(f"{CHARTS_DIR}/product_development.html")
    return fig

def insurance_insights():
    df = fetch(QUERIES["insurance_insights"])
    df["state"] = df["state"].str.replace("-", " ").str.title()
    fig = px.bar(df, x="state", y="total_policies", color="total_amount",
                 title="Insurance Insights: Top 10 States by Insurance Policies",
                 labels={"state": "State", "total_policies": "Total Policies", "total_amount": "Total Amount (₹)"},
                 color_continuous_scale="Oranges")
    fig.update_xaxes(tickangle=45)
    fig.write_html(f"{CHARTS_DIR}/insurance_insights.html")
    return fig

def marketing_optimization():
    df = fetch(QUERIES["marketing_optimization"])
    df["state"] = df["state"].str.replace("-", " ").str.title()
    fig = px.scatter(df, x="total_amount", y="total_users", size="total_users",
                     text="state", color="state",
                     title="Marketing Optimization: High Users vs Low Transaction Amount (Untapped Markets)",
                     labels={"total_amount": "Total Transaction Amount (₹)", "total_users": "Total Registered Users"})
    fig.update_traces(textposition="top center")
    fig.write_html(f"{CHARTS_DIR}/marketing_optimization.html")
    return fig

def trend_analysis():
    df = fetch(QUERIES["trend_analysis"])
    df["quarter_label"] = "Q" + df["quarter"].astype(str) + " " + df["year"].astype(str)
    fig = px.line(df, x="quarter_label", y="total_count", color="transaction_type", markers=True,
                  title="Trend Analysis: Quarter-wise Transaction Volume by Type",
                  labels={"quarter_label": "Quarter", "total_count": "Total Transactions", "transaction_type": "Type"})
    fig.update_xaxes(tickangle=45)
    fig.write_html(f"{CHARTS_DIR}/trend_analysis.html")
    return fig

def competitive_benchmarking():
    df = fetch(QUERIES["competitive_benchmarking"])
    df["entity_name"] = df["entity_name"].str.replace("-", " ").str.title()
    figs = []
    for etype in ["state", "district", "pincode"]:
        dff = df[df["entity_type"] == etype].head(10)
        fig = px.bar(dff, x="total_amount", y="entity_name", orientation="h",
                     title=f"Competitive Benchmarking: Top 10 {etype.title()}s by Transaction Amount",
                     labels={"total_amount": "Total Amount (₹)", "entity_name": etype.title()},
                     color="total_amount", color_continuous_scale="Purples")
        fig.write_html(f"{CHARTS_DIR}/competitive_benchmarking_{etype}.html")
        figs.append(fig)
    return figs

if __name__ == "__main__":
    print("Generating customer_segmentation..."); customer_segmentation(); print("Done")
    print("Generating fraud_detection..."); fraud_detection(); print("Done")
    print("Generating geographical_insights..."); geographical_insights(); print("Done")
    print("Generating payment_performance..."); payment_performance(); print("Done")
    print("Generating user_engagement..."); user_engagement(); print("Done")
    print("Generating product_development..."); product_development(); print("Done")
    print("Generating insurance_insights..."); insurance_insights(); print("Done")
    print("Generating marketing_optimization..."); marketing_optimization(); print("Done")
    print("Generating trend_analysis..."); trend_analysis(); print("Done")
    print("Generating competitive_benchmarking..."); competitive_benchmarking(); print("Done")
    print("\nAll 10 charts generated successfully!")