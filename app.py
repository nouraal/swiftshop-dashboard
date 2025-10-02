import dash
import dash_bootstrap_components as dbc

from modules.data_load import load_data
from modules.data_clean import clean
from modules.kpi_calculations import calculate_kpis
from modules.charts import (
    total_sales_chart,
    avg_order_chart,
    rating_distribution_chart,
    category_performance_chart,
    category_sales_per_month_chart,
    rating_pie_chart,
    category_sales_pie_chart
)
from modules.layout import create_layout
from modules.callbacks import register_callbacks

# ======================================================
# ---------------- Initialize App ---------------------
# ======================================================
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)


# ======================================================
# --------------- Load and Clean Data -----------------
# ======================================================
df = load_data()
df = clean(df)  # Clean the data using modules/data_clean.py

# ======================================================
# ---------------- Calculate KPIs ---------------------
# ======================================================
kpis = calculate_kpis(df)

# --- Compute daily average order for chart ---
avg_order_daily = df.groupby("order_date", as_index=False)["total_amount"].mean()

# ======================================================
# ---------------- Create Charts ----------------------
# ======================================================
fig_total_sales = total_sales_chart(kpis["sales_over_time"])
fig_avg_order = avg_order_chart(
    avg_order_daily
)  # Fix KeyError by using avg_order_daily
fig_rating_dist = rating_distribution_chart(df)
fig_category_pie = category_performance_chart(kpis["sales_by_category"])
fig_category_sales_per_month = category_sales_per_month_chart(
    kpis["sales_by_category_quarter"]
)
fig_rating_pie = rating_pie_chart(df)
fig_category_sales_pie = category_sales_pie_chart(df)
# ======================================================
# ----------------- Columns to Show -------------------
# ======================================================
columns_to_show = [
    col for col in df.columns if col not in ["year", "month", "month_name", "period"]
]

# ======================================================
# ------------------- App Layout ----------------------
# ======================================================
layout = create_layout(
    df,
    kpis,
    columns_to_show,
    fig_total_sales,
    fig_avg_order,
    fig_rating_dist,
    fig_category_pie,
    fig_category_sales_per_month,
    fig_rating_pie,
    fig_category_sales_pie
)
app.layout = layout
# ======================================================
# ---------------- Register Callbacks -----------------
# ======================================================
register_callbacks(app, df, columns_to_show, layout)

# ======================================================
# -------------------- Run Server ---------------------
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)

#   app.run(debug=True, use_reloader=False)
#   app.run(debug=True, use_reloader=True)