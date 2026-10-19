# Customer Intelligence Platform

## Project Overview

This project is an end-to-end Customer Intelligence Platform developed using the Brazilian Olist e-commerce dataset. It combines PostgreSQL, SQL, and Power BI to analyse customer purchasing behaviour, spending patterns, segmentation, and repeat purchases.

The objective is to transform raw transactional data into meaningful business insights that support customer understanding, retention analysis, and data-driven decision-making.

The current implementation includes relational database development, SQL-based data transformation and validation, customer segmentation, second-purchase behaviour analysis, and a two-page interactive Power BI dashboard. Future development will explore Python-based analytics and predictive machine learning.
---

## Project Structure

```
customer-intelligence-platform/
│
├── data/
│   └── processed/
│
├── notebooks/
│
├── powerbi/
│   └── powerbi.pbix
│
├── scripts/
│
├── sql/
│   ├── 01_create_customer_table.sql
│   ├── 02_create_remaining_tables.sql
│   ├── 03_customer_spending.sql
│   ├── 04_customer_segmentation.sql
│   ├── 05_data_validation.sql
│   └── 06_second_purchase_analysis.sql
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Current Progress

- Project structure and Git version control established
- Olist dataset imported into PostgreSQL
- Customer spending and segmentation analysis completed using SQL
- Data validation queries created
- Customer purchase frequency and second-purchase behaviour analysed
- Average and median days to second purchase calculated and validated
- Two-page Power BI dashboard developed:
  - Customer Overview
  - Customer Behaviour & Retention
- Key customer purchasing and retention insights documented

---

## Next Development Stages

- Expand exploratory data analysis using Python and Pandas
- Develop additional customer behaviour and retention analyses
- Explore customer lifetime value (CLV) estimation
- Engineer customer-level features for predictive modelling
- Develop and evaluate machine learning models for repeat-purchase prediction
- Enhance the Power BI dashboard with additional business insights
- Document model performance, analytical limitations, and business recommendations

---

## Technologies Used
- SQL
- PostgreSQL
- Power BI Desktop
- Git and GitHub
- Visual Studio Code

**Technologies Planned for Future Development**
- Python
- Pandas and NumPy
- Scikit-learn
- Matplotlib

## Author

**Esther A**
