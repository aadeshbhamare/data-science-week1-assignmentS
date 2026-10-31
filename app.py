import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📊", layout="wide")

DEFAULT_FILE = Path(__file__).parent / "data" / "cleaned" / "cleaned_sales_dataset.csv"

st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive dashboard generated from your sales analysis dataset")

with st.sidebar:
    st.header("Dashboard Controls")
    uploaded_file = st.file_uploader("Upload an updated CSV file (optional)", type=["csv"])
    if st.button("🔄 Refresh dashboard", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

@st.cache_data
def load_data(file_bytes=None, file_path=None, modified_time=None):
    if file_bytes is not None:
        from io import BytesIO
        data = pd.read_csv(BytesIO(file_bytes))
    else:
        data = pd.read_csv(file_path)
    data.columns = [str(c).strip().lower().replace(" ", "_") for c in data.columns]
    if "order_date" in data.columns:
        data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
    for col in ["quantity", "unit_price", "total_price"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")
    return data

try:
    if uploaded_file is not None:
        df = load_data(file_bytes=uploaded_file.getvalue())
        st.sidebar.success("Using uploaded CSV")
    elif DEFAULT_FILE.exists():
        df = load_data(file_path=str(DEFAULT_FILE), modified_time=DEFAULT_FILE.stat().st_mtime)
    else:
        st.error("Dataset file not found. Keep cleaned_sales_dataset.csv in data/cleaned/.")
        st.stop()
except Exception as exc:
    st.error(f"Could not read the dataset: {exc}")
    st.stop()

required = ["total_price", "quantity"]
missing = [c for c in required if c not in df.columns]
if missing:
    st.error("Missing required columns: " + ", ".join(missing))
    st.write("Columns found:", list(df.columns))
    st.stop()

with st.sidebar:
    st.subheader("Filters")
    filtered = df.copy()
    if "order_date" in filtered.columns and filtered["order_date"].notna().any():
        min_date = filtered["order_date"].min().date()
        max_date = filtered["order_date"].max().date()
        date_range = st.date_input("Order date range", value=(min_date, max_date),
                                   min_value=min_date, max_value=max_date)
        if isinstance(date_range, tuple) and len(date_range) == 2:
            start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1]) + pd.Timedelta(days=1)
            filtered = filtered[(filtered["order_date"] >= start) & (filtered["order_date"] < end)]
    for col, label in [("product_category", "Product category"),
                       ("payment_type", "Payment type"),
                       ("order_status", "Order status")]:
        if col in filtered.columns:
            options = sorted(filtered[col].dropna().astype(str).unique().tolist())
            selected = st.multiselect(label, options, default=options)
            filtered = filtered[filtered[col].astype(str).isin(selected)]

if filtered.empty:
    st.warning("No rows match the selected filters. Change or clear the filters.")
    st.stop()

sales = filtered["total_price"].sum()
orders = filtered["order_id"].nunique() if "order_id" in filtered.columns else len(filtered)
units = filtered["quantity"].sum()
aov = sales / orders if orders else 0
customers = filtered["customer_id"].nunique() if "customer_id" in filtered.columns else None

kpis = st.columns(4 if customers is None else 5)
kpis[0].metric("Total Sales", f"{sales:,.2f}")
kpis[1].metric("Total Orders", f"{orders:,.0f}")
kpis[2].metric("Units Sold", f"{units:,.0f}")
kpis[3].metric("Average Order Value", f"{aov:,.2f}")
if customers is not None:
    kpis[4].metric("Unique Customers", f"{customers:,.0f}")

st.divider()
left, right = st.columns(2)

if "product_category" in filtered.columns:
    category = filtered.groupby("product_category", dropna=False)["total_price"].sum().sort_values(ascending=False).reset_index()
    with left:
        st.subheader("Sales by Product Category")
        fig = px.bar(category, x="product_category", y="total_price", color="product_category",
                     labels={"product_category": "Category", "total_price": "Sales"},
                     title="Revenue by Category")
        fig.update_layout(showlegend=False, xaxis_tickangle=-25)
        st.plotly_chart(fig, use_container_width=True)

if "order_date" in filtered.columns:
    dated = filtered.dropna(subset=["order_date"]).copy()
    if not dated.empty:
        dated["month"] = dated["order_date"].dt.to_period("M").astype(str)
        monthly = dated.groupby("month", as_index=False)["total_price"].sum()
        with right:
            st.subheader("Monthly Sales Trend")
            fig = px.line(monthly, x="month", y="total_price", markers=True,
                          labels={"month": "Month", "total_price": "Sales"},
                          title="Sales Over Time")
            st.plotly_chart(fig, use_container_width=True)

left2, right2 = st.columns(2)
if "order_status" in filtered.columns:
    status = filtered["order_status"].astype(str).value_counts().rename_axis("order_status").reset_index(name="orders")
    with left2:
        st.subheader("Order Status Distribution")
        fig = px.pie(status, names="order_status", values="orders", hole=0.45,
                     labels={"order_status": "Order status", "orders": "Orders"})
        st.plotly_chart(fig, use_container_width=True)

if "payment_type" in filtered.columns:
    payment = filtered.groupby("payment_type", as_index=False).agg(
        sales=("total_price", "sum"),
        orders=("order_id", "nunique") if "order_id" in filtered.columns else ("total_price", "count")
    ).sort_values("sales", ascending=False)
    with right2:
        st.subheader("Sales by Payment Type")
        fig = px.bar(payment, x="payment_type", y="sales", color="payment_type",
                     labels={"payment_type": "Payment type", "sales": "Sales"})
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.divider()
st.subheader("Top Products by Sales")
if "product_id" in filtered.columns:
    products = filtered.groupby("product_id", as_index=False).agg(
        sales=("total_price", "sum"),
        units=("quantity", "sum")
    ).sort_values("sales", ascending=False).head(10)
    st.dataframe(products, use_container_width=True, hide_index=True)
else:
    st.info("No product_id column found, so product ranking is unavailable.")

with st.expander("View filtered data"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)

st.download_button(
    "⬇️ Download filtered data as CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
st.caption(f"Showing {len(filtered):,} of {len(df):,} rows. To use new source data, replace the CSV in data/cleaned/ and click Refresh dashboard.")
