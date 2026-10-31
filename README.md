# Data Science Week 1 Assignment – E-commerce Sales Analysis

## Project Overview
This project focuses on cleaning, analyzing, and visualizing an e-commerce sales dataset using Python. The objective is to identify sales patterns, understand customer behavior, and generate meaningful business insights through data analysis.

## Objectives
- Inspect the dataset and understand its structure.
- Identify missing values, duplicate records, and invalid data.
- Clean and validate the dataset.
- Calculate key performance indicators (KPIs).
- Analyze monthly sales trends, product categories, payment methods, and order statuses.
- Create charts and a dashboard to communicate findings.
- Prepare a final report with business insights and recommendations.

## Tools and Technologies
- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Google Colab
- GitHub
- ReportLab (PDF report generation)

## Dataset Overview
- **Dataset:** E-commerce Sales Dataset
- **Total Records:** 10,000
- **Original Columns:** 10
- **Date Range:** January 1, 2023 – December 31, 2023
- **Missing Values:** 0
- **Exact Duplicate Rows:** 0

The dataset contains order IDs, product IDs, product categories, quantities, unit prices, total prices, order dates, customer IDs, payment types, and order statuses.

## Data Cleaning and Validation
The following checks were performed:
- Inspected column names, data types, and dataset dimensions.
- Checked missing values and exact duplicate records.
- Checked repeated order IDs.
- Converted order dates to datetime format and validated dates.
- Checked for negative or zero quantities and prices.
- Verified total price consistency using quantity × unit price.
- Standardized column names for easier analysis.

No missing values, exact duplicate rows, invalid dates, negative quantities, or zero prices were found in the validation checks.

## Analysis Performed
- Total recorded order value and other KPIs.
- Average order value (AOV).
- Total units and unique customers.
- Category-wise revenue analysis.
- Top revenue-generating product analysis.
- Monthly and weekly recorded order-value trends.
- Order status distribution.
- Payment method distribution.
- Customer spending analysis.

## Visualizations
The project includes:
- Category-wise Revenue Bar Chart
- Monthly Sales Trend Line Chart
- Order Status Distribution Pie Chart
- Payment Type Bar Chart
- Combined Sales Dashboard

Visualizations are available in the `outputs/` directory.

## Interactive Dashboard
Run the Streamlit dashboard from the repository root:

```bash
pip install -r requirements.txt
streamlit run app.py
```

The dashboard loads `data/cleaned/cleaned_sales_dataset.csv` by default. You can also upload a CSV from the dashboard sidebar.

## Repository Structure
```text
data-science-week1-assignment/
├── data/
│   ├── raw/
│   └── cleaned/
├── notebooks/
│   └── week1_analysis.ipynb
├── outputs/
│   ├── charts/
│   └── dashboard/
├── reports/
│   └── final_report.pdf
├── app.py
├── screenshots/
├── README.md
└── requirements.txt
```

## Key Findings
The analysis compares revenue across product categories, examines monthly and weekly patterns, and summarizes order statuses, payment methods, and customer spending. The notebook and final report contain the calculated KPIs and detailed observations.

## Recommendations
- Monitor monthly and weekly trends to support sales planning.
- Compare category performance to identify opportunities for improvement.
- Review order statuses to understand cancellations, refunds, and pending orders.
- Use customer spending insights to plan customer-retention strategies.
- Continue validating data quality before making business decisions.

## Limitations and Assumptions
- The dataset covers the period from January to December 2023.
- Revenue calculations use the recorded `total_price` values across all order statuses, including pending, cancelled, and refunded orders. Therefore, these values represent **recorded order value**, not confirmed completed-sales revenue.
- Findings are limited to the fields available in the dataset.

## Deliverables
- Raw and cleaned datasets
- Jupyter Notebook containing the analysis
- Sales charts and dashboard
- Final PDF report

## Author
**Aadesh Bhamare**

## Disclaimer
This project was completed for educational purposes as part of a Data Science Week 1 internship assignment.
