# queries.py
# Contains all 10 SQL queries as a dictionary, imported by analysis.py and app.py.

QUERIES = {
    "customer_segmentation": """
        SELECT state, SUM(registered_users) AS total_users
        FROM aggregated_user
        GROUP BY state
        ORDER BY total_users DESC
        LIMIT 10
    """,

    "fraud_detection": """
        SELECT state, SUM(transaction_count) AS total_count,
        ROUND(SUM(transaction_amount),2) AS total_amount,
        ROUND(SUM(transaction_amount)/SUM(transaction_count),2) AS avg_amount_per_txn
        FROM aggregated_transaction
        GROUP BY state
        ORDER BY total_count DESC, avg_amount_per_txn ASC
        LIMIT 10
    """,

    "geographical_insights": """
        SELECT state, SUM(transaction_count) AS total_count,
        ROUND(SUM(transaction_amount),2) AS total_amount
        FROM map_transaction
        GROUP BY state
        ORDER BY total_amount DESC
        LIMIT 10
    """,

    "payment_performance": """
        SELECT transaction_type, SUM(transaction_count) AS total_count,
        ROUND(SUM(transaction_amount),2) AS total_amount
        FROM aggregated_transaction
        GROUP BY transaction_type
        ORDER BY total_count DESC
    """,

    "user_engagement": """
        SELECT state, year, SUM(registered_users) AS total_users
        FROM aggregated_user
        GROUP BY state, year
        ORDER BY state, year
    """,

    "product_development": """
        SELECT year, quarter, SUM(transaction_count) AS total_count,
        ROUND(SUM(transaction_amount),2) AS total_amount
        FROM aggregated_transaction
        GROUP BY year, quarter
        ORDER BY year, quarter
    """,

    "insurance_insights": """
        SELECT state, SUM(insurance_count) AS total_policies,
        ROUND(SUM(insurance_amount),2) AS total_amount
        FROM aggregated_insurance
        GROUP BY state
        ORDER BY total_policies DESC
        LIMIT 10
    """,

    "marketing_optimization": """
        SELECT au.state,
        SUM(au.registered_users) AS total_users,
        ROUND(SUM(at.transaction_amount),2) AS total_amount
        FROM aggregated_user au
        JOIN aggregated_transaction at ON au.state = at.state
        GROUP BY au.state
        ORDER BY total_users DESC, total_amount ASC
        LIMIT 10
    """,

    "trend_analysis": """
        SELECT year, quarter, transaction_type,
        SUM(transaction_count) AS total_count,
        ROUND(SUM(transaction_amount),2) AS total_amount
        FROM aggregated_transaction
        GROUP BY year, quarter, transaction_type
        ORDER BY year, quarter, total_count DESC
    """,

    "competitive_benchmarking": """
        SELECT * FROM (
            SELECT 'state' AS entity_type, state AS entity_name,
            SUM(transaction_count) AS total_count,
            ROUND(SUM(transaction_amount),2) AS total_amount
            FROM top_transaction WHERE entity_type='district'
            GROUP BY state ORDER BY total_amount DESC LIMIT 10
        ) a
        UNION ALL
        SELECT * FROM (
            SELECT 'district', entity_name,
            SUM(transaction_count), ROUND(SUM(transaction_amount),2)
            FROM top_transaction WHERE entity_type='district'
            GROUP BY entity_name ORDER BY SUM(transaction_amount) DESC LIMIT 10
        ) b
        UNION ALL
        SELECT * FROM (
            SELECT 'pincode', entity_name,
            SUM(transaction_count), ROUND(SUM(transaction_amount),2)
            FROM top_transaction WHERE entity_type='pincode'
            GROUP BY entity_name ORDER BY SUM(transaction_amount) DESC LIMIT 10
        ) c
    """
}