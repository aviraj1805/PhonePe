# PhonePe Transaction Insights Dashboard

A data analysis and visualization project built on the PhonePe Pulse dataset. It extracts transaction, user, and insurance data across all Indian states from 2018 to 2024, loads it into a relational database, and presents insights through an interactive multi-page Streamlit dashboard.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture and Workflow](#architecture-and-workflow)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dashboard Pages](#dashboard-pages)
- [Key Insights](#key-insights)
- [Data Source](#data-source)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Problem Statement

Digital payment platforms generate large volumes of transaction data that, when analyzed systematically, can reveal patterns in user behavior, regional adoption, payment category distribution, and potential fraud signals. This project processes PhonePe's publicly released Pulse data to surface actionable insights across states, districts, and time periods — supporting decisions in marketing, product development, risk assessment, and operational planning.

---

## Features

- ETL pipeline to extract and load PhonePe Pulse JSON data into MySQL
- Nine structured database tables covering aggregated, map-level, and top-performer data
- Ten SQL queries addressing distinct business questions
- Interactive choropleth map visualizing transaction distribution at the state level
- Dynamic business insights generated from query results
- Multi-page Streamlit dashboard covering transactions, users, insurance, and risk detection
- Fraud and anomaly detection through pattern-based analysis

---

## Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.10+ |
| Database | MySQL |
| Data Processing | Pandas |
| Visualization | Plotly |
| Dashboard | Streamlit |
| DB Connectivity | mysql-connector-python |
| Mapping | GeoJSON via Requests |
| Version Control | Git |

---

## Architecture and Workflow

```
PhonePe Pulse GitHub Repository (JSON)
        |
        v
  Data Extraction (Python)
        |
        v
  MySQL Database (9 Tables)
        |
        v
  SQL Query Layer (queries.py)
        |
        v
  Analysis and Chart Generation (analysis.py)
        |
        v
  Insights Engine (insights.py)
        |
        v
  Streamlit Dashboard (app.py) — 5 Pages
```

### Database Table Structure

**Aggregated Tables**
- `aggregated_transaction` — Payment category totals by state and quarter
- `aggregated_user` — User registration and app opens by state and quarter
- `aggregated_insurance` — Insurance transaction totals by state and quarter

**Map Tables**
- `map_transaction` — District-level transaction amounts
- `map_user` — District-level user counts
- `map_insurance` — District-level insurance data

**Top Tables**
- `top_transaction` — Top states, districts, and pin codes by transaction amount
- `top_user` — Top states and districts by registered user count
- `top_insurance` — Top states and districts by insurance policy count

---

## Project Structure

```
PhonePe/
├── app.py                  # Streamlit dashboard entry point (5 pages)
├── analysis.py             # Chart generation functions (10 charts)
├── queries.py              # SQL query definitions as a dictionary
├── db_config_template.py   # Database connection configuration template
├── insights.py             # Dynamic insights generator
├── requirements.txt        # Python dependencies
├── documentation.md        # Technical documentation
├── README.md               # Project overview
└── .gitignore
```

---

## Installation

### Prerequisites

- Python 3.10 or higher
- MySQL 8.0 or higher
- Git

### Steps

**1. Clone this repository**

```bash
git clone https://github.com/aviraj1805/PhonePe.git
cd PhonePe
```

**2. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**3. Clone the PhonePe Pulse data repository**

```bash
git clone https://github.com/PhonePe/pulse.git
```

**4. Set up the MySQL database**

```sql
CREATE DATABASE phonepe_pulse;
```

**5. Configure database credentials**

Copy the template and update it with your credentials:

```bash
cp db_config_template.py db_config.py
```

Edit `db_config.py`:

```python
DB_CONFIG = {
    "host": "localhost",
    "user": "your_mysql_user",
    "password": "your_mysql_password",
    "database": "phonepe_pulse"
}
```

**6. Load data into MySQL**

```bash
python load_data.py
```

**7. Launch the dashboard**

```bash
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`.

---

## Configuration

The `db_config_template.py` file provides the expected structure for database credentials. Create a local `db_config.py` from this template and ensure it is listed in `.gitignore` to avoid committing credentials.

Environment variables can alternatively be used in place of a config file:

```bash
export DB_HOST=localhost
export DB_USER=your_user
export DB_PASSWORD=your_password
export DB_NAME=phonepe_pulse
```

---

## Usage

Once the dashboard is running:

1. Navigate to `http://localhost:8501` in your browser.
2. Use the sidebar to switch between dashboard pages.
3. Apply filters (state, year, quarter) where available to drill down into specific segments.
4. Charts are interactive — hover for exact values, click legends to filter series.


---

## Key Insights

- Telangana leads all states with approximately 41,65,595 Cr in cumulative transaction amount.
- Merchant Payments is the dominant payment category, accounting for over 130 billion transactions.
- Q4 2024 recorded the highest single-quarter transaction volume in the dataset.
- Uttar Pradesh recorded the highest registered user growth in the most recent year analyzed.
- Maharashtra presents an untapped market signal — high registered users but comparatively low transaction amount per user.
- Karnataka leads insurance adoption with approximately 19,57,404 total policies.
- PhonePe transaction volume grew approximately 91.9x between 2018 and 2024.
- Bengaluru Urban is the top-performing district with approximately 19,93,784 Cr in total transactions.

---

## Data Source

The dataset is sourced from the official **PhonePe Pulse** open data repository:

- Repository: [https://github.com/PhonePe/pulse](https://github.com/PhonePe/pulse)
- Coverage: All Indian states and union territories
- Period: 2018 Q1 to 2024 Q4
- Data categories: Transactions, Users, Insurance

The data is structured as JSON files organized by year and quarter, which this project parses and loads into a relational schema.

---

## Future Improvements

- Automate periodic data sync from the PhonePe Pulse repository using a scheduled job
- Add PostgreSQL support alongside the existing MySQL backend
- Introduce district-level choropleth maps for more granular geographic analysis
- Implement a forecasting module using time-series models for transaction projections
- Add export functionality (CSV, PDF) for charts and insight summaries
- Deploy the dashboard to a cloud platform (Streamlit Cloud, AWS, or GCP)
- Enhance the fraud detection module with statistical outlier methods

---

## License

This project is for educational and analytical purposes. The underlying PhonePe Pulse data is published under the terms defined by PhonePe at [https://github.com/PhonePe/pulse](https://github.com/PhonePe/pulse).

---

## Contact

**Author:** Aviraj  
**GitHub:** [https://github.com/aviraj1805](https://github.com/aviraj1805)  
**Business Case Study Reference:** [SQL Query Documentation](https://docs.google.com/document/d/1cadU8MeuU575sV3V6Pne37MJLR1VpP82X6YBUV_owCY/edit?usp=sharing)
