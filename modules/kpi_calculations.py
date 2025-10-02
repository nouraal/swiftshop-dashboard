# modules/kpi_calculations.py
# ======================================================
# ---------------- KPI Calculations -------------------
# ======================================================

import pandas as pd


def calculate_kpis(df):
    """
    Calculate key performance indicators and chart data from the dataframe.
    Returns a dict with KPI values formatted for display and raw data for charts.
    """

    if df is None or df.empty:
        return {
            # --- Summary KPIs (for cards) ---
            "total_sales": "SAR 0",
            "total_orders": "0",
            "avg_order_value": "SAR 0.00",
            "avg_rating": "N/A",
            # --- Chart data ---
            "sales_over_time": pd.DataFrame(),
            "sales_by_region": pd.DataFrame(),
            "sales_by_category": pd.DataFrame(),
            "orders_by_payment": pd.DataFrame(),
            "top_products": pd.DataFrame(),
            "avg_rating_region": pd.DataFrame(),
        }

    # ======================================================
    # ---------------- Summary KPI Cards ------------------
    # ======================================================

    # --- Total Sales ---
    total_sales = df["total_amount"].sum() if "total_amount" in df.columns else 0
    total_sales_text = f"SAR {total_sales:,.0f}"

    # --- Total Orders ---
    total_orders = int(df.shape[0])
    total_orders_text = f"{total_orders:,}"

    # --- Average Order Value ---
    avg_order_value = df["total_amount"].mean() if "total_amount" in df.columns else 0
    avg_order_value_text = f"SAR {avg_order_value:,.2f}"

    # --- Average Rating ---
    avg_rating = (
        df["customer_rating"].mean() if "customer_rating" in df.columns else None
    )
    avg_rating_text = f"{avg_rating:.1f}" if avg_rating is not None else "N/A"

    # --- Sales by Category per Month ---
    sales_by_category_month = (
        df.groupby(["year", "month", "category"], as_index=False)["total_amount"].sum()
        if {"year", "month", "category", "total_amount"}.issubset(df.columns)
        else pd.DataFrame()
    )

    if not sales_by_category_month.empty:
        sales_by_category_month["period"] = (
            sales_by_category_month["year"].astype(str)
            + "-"
            + sales_by_category_month["month"].astype(str)
        )

    # --- Sales by Category per Quarter ---
    if {"year", "month", "category", "total_amount"}.issubset(df.columns):
        sales_by_category_quarter = (
            df.copy()
            .assign(
                quarter=lambda x: ((x["month"] - 1) // 3 + 1)
            )  # Convert month to quarter
            .groupby(["year", "quarter", "category"], as_index=False)["total_amount"]
            .sum()
        )

        # Add readable period label for charts
        sales_by_category_quarter["period"] = (
            "Q"
            + sales_by_category_quarter["quarter"].astype(str)
            + " "
            + sales_by_category_quarter["year"].astype(str)
        )
    else:
        sales_by_category_quarter = pd.DataFrame()

    # ======================================================
    # ---------------- Chart Data -------------------------
    # ======================================================

    # --- Sales Over Time ---
    sales_over_time = (
        df.groupby("order_date", as_index=False)["total_amount"].sum()
        if "order_date" in df.columns
        else pd.DataFrame()
    )

    # --- Sales by Region ---
    sales_by_region = (
        df.groupby("customer_region", as_index=False)["total_amount"].sum()
        if "customer_region" in df.columns
        else pd.DataFrame()
    )

    # --- Sales by Category ---
    sales_by_category = (
        df.groupby("category", as_index=False)["total_amount"].sum()
        if "category" in df.columns
        else pd.DataFrame()
    )

    # --- Orders by Payment Method ---
    orders_by_payment = (
        df["payment_method"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "payment_method", "payment_method": "count"})
        if "payment_method" in df.columns
        else pd.DataFrame()
    )

    # --- Top Products ---
    top_products = (
        df.groupby("product_name", as_index=False)["total_amount"]
        .sum()
        .sort_values("total_amount", ascending=False)
        .head(10)
        if "product_name" in df.columns
        else pd.DataFrame()
    )

    # --- Average Rating by Region ---
    avg_rating_region = (
        df.groupby("customer_region", as_index=False)["customer_rating"].mean()
        if "customer_rating" in df.columns and "customer_region" in df.columns
        else pd.DataFrame()
    )

    return {
        # --- Summary KPIs ---
        "total_sales": total_sales_text,
        "total_orders": total_orders_text,
        "avg_order_value": avg_order_value_text,
        "avg_rating": avg_rating_text,
        "total_sales": total_sales_text,
        "sales_by_category": sales_by_category,
        "sales_by_category_month": sales_by_category_month,
        # --- Chart Data ---
        "sales_over_time": sales_over_time,
        "sales_by_region": sales_by_region,
        "sales_by_category": sales_by_category,
        "orders_by_payment": orders_by_payment,
        "top_products": top_products,
        "avg_rating_region": avg_rating_region,
        "sales_by_category_quarter": sales_by_category_quarter,
    }
