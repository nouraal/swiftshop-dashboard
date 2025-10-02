import plotly.express as px
from modules.style import CHART_LAYOUT, CHART_LINE_COLOR, CHART_MARKER_COLOR


def total_sales_chart(sales_over_time):
    fig = px.line(
        sales_over_time,
        x="order_date",
        y="total_amount",
        title="Total Sales Over Time",
        markers=True,
        labels={"order_date": "Date", "total_amount": "Sales (SAR)"},
    )
    fig.update_traces(line_color=CHART_LINE_COLOR, marker_color=CHART_MARKER_COLOR)
    fig.update_layout(**CHART_LAYOUT)
    return fig


def avg_order_chart(avg_order_daily):
    fig = px.line(
        avg_order_daily,
        x="order_date",
        y="total_amount",
        title="Average Order Value Over Time",
        markers=True,
        labels={"order_date": "Date", "total_amount": "Sales (SAR)"},
    )
    fig.update_traces(line_color=CHART_LINE_COLOR, marker_color=CHART_MARKER_COLOR)
    fig.update_layout(**CHART_LAYOUT)
    return fig


def rating_distribution_chart(df):
    fig = px.histogram(
        df,
        x="customer_rating",
        nbins=5,
        title="Customer Rating",
        color="customer_rating",
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig


def category_performance_chart(sales_by_category):
    fig = px.pie(
        sales_by_category,
        names="category",
        values="total_amount",
        title="Product Category Performance",
    )
    fig.update_layout(**CHART_LAYOUT)
    return fig


def category_sales_per_month_chart(sales_by_category_quarter):
    if sales_by_category_quarter.empty:
        return px.bar(title="No data available")

    fig = px.bar(
        sales_by_category_quarter,
        x="period",
        y="total_amount",
        color="category",
        barmode="stack",
        text_auto=True,
        labels={"period": "Date", "total_amount": "Sales (SAR)"},
        title="Quarterly Sales by Category",
        color_discrete_map={
            "Electronics": "#5879FF",
            "Clothing": "#A66DD4",
            "Home Goods": "#D9B5C1",
            "Other": "#C2CFF3",
        },
    )
    fig.update_layout(
        xaxis=dict(title=""),
        yaxis=dict(range=[0, sales_by_category_quarter["total_amount"].max() * 1.25]),
        bargap=0,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),
        **CHART_LAYOUT,
    )
    return fig


def rating_pie_chart(df):
    if "customer_rating" not in df.columns or df.empty:
        return px.pie(title="No rating data available")

    rating_counts = df["customer_rating"].value_counts().reset_index()
    rating_counts.columns = ["rating", "count"]

    fig = px.pie(
        rating_counts,
        names="rating",
        values="count",
        title="Customer Ratings",
        hole=0.3,
        color="rating",
        color_discrete_map={
            1: "#5879FF",
            2: "#C2CFF3",
            3: "#5246AB",
            4: "#D9B5C1",
            5: "#A66DD4",
        },
    )
    fig.update_layout(**CHART_LAYOUT)
    fig.update_traces(textinfo="percent+label")
    return fig


# Pie chart of sales percentage by category
def category_sales_pie_chart(df):
    if {"category", "total_amount"}.issubset(df.columns) and not df.empty:
        sales_by_category = df.groupby("category", as_index=False)["total_amount"].sum()
        fig = px.pie(
            sales_by_category,
            names="category",
            values="total_amount",
            title="Sales by Category",
            # hole=0.3,
            color="category",
            color_discrete_map={
                "Electronics": "#5879FF",
                "Clothing": "#D9B5C1",
                "Home Goods": "#C2CFF3",
                "Other": "#A66DD4",
            },
        )
        # ------ Merge layout ---------------------

        fig.update_traces(textinfo="percent+label")
        layout_updates = dict(CHART_LAYOUT)
        layout_updates.update(
            margin=dict(l=10, r=10, t=40, b=10), paper_bgcolor="white"
        )
        fig.update_layout(**layout_updates)
        return fig
    else:
        return px.pie(title="No category sales data available")
