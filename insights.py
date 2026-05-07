# insights.py
# Dynamically fetches 8 key business insights from the phonepe_pulse database.

from db_connect import get_connection
import pandas as pd

def fetch(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(cursor.fetchall(), columns=columns)
    cursor.close()
    conn.close()
    return df

def generate_insights():
    df1 = fetch("SELECT state, ROUND(SUM(transaction_amount)/1e7,2) AS amt_cr FROM aggregated_transaction GROUP BY state ORDER BY amt_cr DESC LIMIT 1")
    top_state = df1["state"][0].replace("-", " ").title()
    top_amt = df1["amt_cr"][0]

    df2 = fetch("SELECT transaction_type, SUM(transaction_count) AS cnt FROM aggregated_transaction GROUP BY transaction_type ORDER BY cnt DESC LIMIT 1")
    top_category = df2["transaction_type"][0]
    top_cat_count = int(df2["cnt"][0])

    df3 = fetch("SELECT year, quarter, SUM(transaction_count) AS cnt FROM aggregated_transaction GROUP BY year, quarter ORDER BY cnt DESC LIMIT 1")
    peak_year = int(df3["year"][0])
    peak_quarter = int(df3["quarter"][0])

    df4 = fetch("SELECT state, year, SUM(registered_users) AS users FROM aggregated_user GROUP BY state, year ORDER BY state, year")
    df4_pivot = df4.pivot(index="state", columns="year", values="users").fillna(0)
    years = sorted(df4_pivot.columns)
    if len(years) >= 2:
        df4_pivot["growth"] = df4_pivot[years[-1]] - df4_pivot[years[-2]]
        fastest_state = df4_pivot["growth"].idxmax().replace("-", " ").title()
    else:
        fastest_state = "N/A"

    df5 = fetch("""
        SELECT au.state, SUM(au.registered_users) AS users,
        ROUND(SUM(at.transaction_amount)/SUM(au.registered_users),2) AS amt_per_user
        FROM aggregated_user au
        JOIN aggregated_transaction at ON au.state = at.state
        GROUP BY au.state ORDER BY users DESC, amt_per_user ASC LIMIT 1
    """)
    underserved = df5["state"][0].replace("-", " ").title()

    df6 = fetch("SELECT state, SUM(insurance_count) AS cnt FROM aggregated_insurance GROUP BY state ORDER BY cnt DESC LIMIT 1")
    top_ins_state = df6["state"][0].replace("-", " ").title()
    top_ins_count = int(df6["cnt"][0])

    df7 = fetch("SELECT year, SUM(transaction_count) AS cnt FROM aggregated_transaction GROUP BY year ORDER BY year")
    first_yr = int(df7["year"].iloc[0])
    last_yr = int(df7["year"].iloc[-1])
    first_cnt = int(df7["cnt"].iloc[0])
    last_cnt = int(df7["cnt"].iloc[-1])
    growth_x = round(last_cnt / first_cnt, 1)

    df8 = fetch("SELECT entity_name, ROUND(SUM(transaction_amount)/1e7,2) AS amt_cr FROM top_transaction WHERE entity_type='district' GROUP BY entity_name ORDER BY amt_cr DESC LIMIT 1")
    top_district = df8["entity_name"][0].replace("-", " ").title()
    top_dist_amt = df8["amt_cr"][0]

    return {
        "top_state": f"{top_state} leads all states with ₹{top_amt} Cr in total transaction amount.",
        "top_category": f"'{top_category}' is the most used payment category with {top_cat_count:,} transactions.",
        "peak_quarter": f"Q{peak_quarter} {peak_year} recorded the highest transaction volume across all years.",
        "fastest_growing": f"{fastest_state} showed the highest user growth in the most recent year.",
        "underserved_market": f"{underserved} has high registered users but low transaction amount per user — a key untapped market.",
        "top_insurance": f"{top_ins_state} leads insurance adoption with {top_ins_count:,} total policies.",
        "overall_growth": f"PhonePe transactions grew {growth_x}x from {first_yr} to {last_yr}, reflecting massive platform adoption.",
        "top_district": f"{top_district} is the top-performing district with ₹{top_dist_amt} Cr in total transactions."
    }

if __name__ == "__main__":
    insights = generate_insights()
    for key, value in insights.items():
        print(f"{key}: {value}")