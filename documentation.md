# PhonePe Transaction Insights — Technical Documentation

## Problem Statement
PhonePe processes billions of digital transactions across India. However, raw transaction data stored across thousands of JSON files is not directly usable for business decision-making. This project solves that by building an end-to-end data pipeline that extracts, stores, analyzes, and visualizes this data in an interactive dashboard — enabling insights on transactions, users, insurance, and risk patterns.

## Approach & Methodology
1. **Data Extraction** — Cloned the official PhonePe Pulse GitHub repository containing 9000+ JSON files organized by category, state, year, and quarter.
2. **Data Storage** — Parsed all JSON files using Python and loaded records into 9 MySQL tables inside the `phonepe_pulse` database.
3. **Query Development** — Wrote 10 optimized SQL queries covering all major business use cases.
4. **Visualization** — Built 10 interactive Plotly charts (bar, scatter, pie, line, choropleth, bubble) using Pandas DataFrames fetched from MySQL.
5. **Dashboard** — Deployed a 5-page Streamlit dashboard with filters, KPI cards, dynamic insights, and data tables.

## Database Schema

| Table | Key Columns |
|-------|-------------|
| aggregated_transaction | state, year, quarter, transaction_type, transaction_count, transaction_amount |
| aggregated_user | state, year, quarter, registered_users, app_opens, device_brand, device_count |
| aggregated_insurance | state, year, quarter, insurance_type, insurance_count, insurance_amount |
| map_transaction | state, year, quarter, district, transaction_count, transaction_amount |
| map_user | state, year, quarter, district, registered_users, app_opens |
| map_insurance | state, year, quarter, district, insurance_count, insurance_amount |
| top_transaction | state, year, quarter, entity_type, entity_name, transaction_count, transaction_amount |
| top_user | state, year, quarter, entity_type, entity_name, registered_users |
| top_insurance | state, year, quarter, entity_type, entity_name, insurance_count, insurance_amount |

## SQL Query Descriptions

| Query | Business Question Answered |
|-------|---------------------------|
| customer_segmentation | Which states have the highest number of registered PhonePe users? |
| fraud_detection | Which states have unusually high transaction count but low average transaction amount? |
| geographical_insights | What is the total transaction volume and amount at the state level across India? |
| payment_performance | Which payment categories (P2P, merchant, recharge) are most popular by volume? |
| user_engagement | How has registered user count grown year-over-year across states? |
| product_development | How do transaction counts and amounts trend across quarters and years? |
| insurance_insights | Which states lead in PhonePe insurance policy adoption? |
| marketing_optimization | Which states have high users but low transaction amount — potential growth markets? |
| trend_analysis | How does transaction volume trend by payment type across all quarters? |
| competitive_benchmarking | What are the top 10 states, districts, and pincodes by total transaction amount? |

## Visualization Choices

| Chart | Reason for Choice |
|-------|------------------|
| Horizontal Bar — Customer Segmentation | Easy state-wise comparison of large user numbers |
| Scatter Plot — Fraud Detection | Reveals outliers between transaction count and average amount |
| Choropleth Map — Geographical Insights | Best for showing state-level data on actual Indian map |
| Pie Chart — Payment Performance | Shows proportional share of each payment category clearly |
| Line Chart — User Engagement | Ideal for showing trends and growth over multiple years |
| Grouped Bar — Product Development | Compares transaction volume across quarters and years side by side |
| Bar Chart — Insurance Insights | Simple comparison of insurance adoption across top states |
| Bubble Chart — Marketing Optimization | Three-dimensional view of users, amount, and state size together |
| Line with Markers — Trend Analysis | Shows volume trends per payment type with clear data points |
| Horizontal Bar — Competitive Benchmarking | Ranked comparison of top 10 entities by transaction amount |

## Challenges Faced & Solutions

| Challenge | Solution |
|-----------|----------|
| JSON files had inconsistent structure across categories | Inspected sample files from each category before writing parsers |
| Insurance data starts from 2020 Q2, not 2018 | Used dynamic file discovery with os.listdir() instead of hardcoded paths |
| Map user JSON uses dict format, not list format | Handled separately with `.items()` iteration instead of list loop |
| pandas read_sql() showed SQLAlchemy warning | Replaced with cursor-based fetching using mysql-connector directly |
| Choropleth map required exact state name matching | Built a manual mapping dictionary from slug names to GeoJSON property names |
| UNION ALL with ORDER BY caused MySQL syntax error | Wrapped each SELECT in a subquery before applying UNION ALL |

## Future Improvements
1. **Real-time Data Updates** — Schedule a cron job to pull latest PhonePe Pulse data weekly and refresh the database automatically.
2. **District-level Choropleth Map** — Add a second map chart showing district-level transaction density using a district-level GeoJSON for India.
3. **Predictive Analytics** — Use time-series forecasting (Prophet or ARIMA) to predict next quarter's transaction volume by state.
4. **User Device Analysis** — Add a dedicated page analyzing which mobile brands dominate PhonePe usage in each state.
5. **Export Feature** — Add a "Download CSV" button on every dashboard page so analysts can export filtered data directly.