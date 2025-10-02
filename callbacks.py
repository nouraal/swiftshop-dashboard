import dash
from dash import Input, Output, State, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.style import CHART_LAYOUT


def register_callbacks(app, df, columns_to_show, layout):
    # ======================================================
    # ------------- Page Navigation Callback --------------
    # ======================================================
    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def display_page(pathname):
        return layout.page_dict.get(pathname, layout.page_dict["/"])

    # ======================================================
    # ------------- Dashboard Filters Callback -----------
    # ======================================================
    @app.callback(
        Output("filters-div", "style"),
        Input("toggle-filters", "n_clicks"),
        State("filters-div", "style"),
    )
    def toggle_filters(n_clicks, current_style):
        if n_clicks:
            if current_style and current_style.get("display") == "none":
                return {"display": "block"}
        else:
            return {"display": "none"}
        return {"display": "none"}

    @app.callback(
        Output("sales-line", "figure"),
        Output("top-products", "figure"),
        Output("orders-table", "data"),
        Output("filtered-data", "data"),
        Input("date-picker", "start_date"),
        Input("date-picker", "end_date"),
        Input("region-dropdown", "value"),
        Input("category-dropdown", "value"),
    )
    def update_dashboard(start_date, end_date, selected_regions, selected_categories):
        filtered_df = df.copy()

        # --- Date Filter ---
        if start_date and end_date and "year" in df.columns and "month" in df.columns:
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            filtered_df = filtered_df[
                (
                    (df["year"] > start_date.year)
                    | (
                        (df["year"] == start_date.year)
                        & (df["month"] >= start_date.month)
                    )
                )
                & (
                    (df["year"] < end_date.year)
                    | ((df["year"] == end_date.year) & (df["month"] <= end_date.month))
                )
            ]

        # --- Region Filter ---
        if selected_regions and "customer_region" in filtered_df.columns:
            filtered_df = filtered_df[
                filtered_df["customer_region"].isin(selected_regions)
            ]

        # --- Category Filter ---
        if selected_categories and "category" in filtered_df.columns:
            filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

        # --- Sales Over Time Chart ---
        if (
            not filtered_df.empty
            and "year" in filtered_df.columns
            and "month" in filtered_df.columns
        ):
            sales_over_time = filtered_df.groupby(["year", "month"], as_index=False)[
                "total_amount"
            ].sum()
            sales_over_time["period"] = (
                sales_over_time["year"].astype(str)
                + "-"
                + sales_over_time["month"].astype(str)
            )
            sales_over_time["MoM_change"] = (
                sales_over_time["total_amount"].pct_change() * 100
            )
            sales_over_time["YoY_change"] = (
                sales_over_time["total_amount"].pct_change(12) * 100
            )

            # --- Base figure ---
            fig_line = go.Figure()

            # Bar for Total Sales
            fig_line.add_trace(
                go.Bar(
                    x=sales_over_time["period"],
                    y=sales_over_time["total_amount"],
                    name="Total Sales",
                    marker_color="#5879FF",
                    hovertemplate="Sales: %{y:,.2f}<extra></extra>",
                    marker=dict(cornerradius="15%"),
                )
            )

            # Line for MoM change
            fig_line.add_trace(
                go.Scatter(
                    x=sales_over_time["period"],
                    y=sales_over_time["MoM_change"],
                    mode="lines+markers",
                    name="Month over Month Change",
                    yaxis="y2",
                    hovertemplate="%{y:.2f}%<extra></extra>",
                    line_shape="spline",
                    line=dict(color="#D9B5C1"),
                )
            )
            # Line for YoY change
            fig_line.add_trace(
                go.Scatter(
                    x=sales_over_time["period"],
                    y=sales_over_time["YoY_change"],
                    mode="lines+markers",
                    name="Year over Year Change",
                    yaxis="y2",
                    hovertemplate="%{y:.2f}%<extra></extra>",
                    line_shape="spline",
                    line=dict(color="#A66DD4"),
                )
            )

            # --- Layout with dual y-axis
            line_layout = dict(CHART_LAYOUT)
            line_layout.update(
                title="Sales Growth",
                xaxis_title="",
                xaxis=dict(title=""),
                yaxis=dict(title=""),
                yaxis2=dict(
                    title="",
                    overlaying="y",
                    side="right",
                    showgrid=False,
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.05,
                    xanchor="center",
                    x=0.5,
                ),
                barmode="group",
            )
            fig_line.update_layout(**line_layout)

        else:
            fig_line = go.Figure().update_layout(title="Total Sales Over Time")

        # --- Top Products Chart ---
        if not filtered_df.empty and "product_name" in filtered_df.columns:
            top_products = (
                filtered_df.groupby("product_name", as_index=False)["total_amount"]
                .sum()
                .sort_values(by="total_amount", ascending=False)
                .head(10)
            )

            fig_top = px.bar(
                top_products,
                x="total_amount",
                y="product_name",
                orientation="h",  # horizontal bars
                title="Top 10 Products by Sales",
                hover_data={"total_amount": ":,.2f"},
            )

            # Highest on top
            fig_top.update_yaxes(categoryorder="total ascending")
            fig_top.update_layout(**CHART_LAYOUT)

            # Show total above bars
            fig_top.update_traces(
                text=top_products["total_amount"].astype(int),
                texttemplate="%{text:,}",
                textposition="outside",
                marker=dict(
                    color=[
                        "#5246AB",
                        "#5879FF",
                        "#A66DD4",
                        "#C2CFF3",
                        "#D9B5C1",
                        "#5246AB",
                        "#5879FF",
                        "#A66DD4",
                        "#C2CFF3",
                        "#D9B5C1",
                    ],
                    cornerradius="15%",
                ),
            )

            # Adjust x-axis for space above bars
            fig_top.update_layout(**CHART_LAYOUT)
            fig_top.update_layout(
                xaxis=dict(range=[0, top_products["total_amount"].max() * 1.25]),
                yaxis=dict(title=""),
                xaxis_title="",
            )

        else:
            fig_top = px.bar(title="Top 10 Products by Sales")

        # --- Orders Table Data ---
        filtered_table_df = (
            filtered_df.copy()
            if not filtered_df.empty
            else pd.DataFrame(columns=columns_to_show)
        )

        if "order_date" in filtered_table_df.columns:
            filtered_table_df["order_date"] = pd.to_datetime(
                filtered_table_df["order_date"]
            ).dt.strftime("%Y-%m-%d")

        return (
            fig_line,
            fig_top,
            filtered_table_df.to_dict("records"),
            filtered_df.to_dict("records"),
        )

    # ======================================================
    # ------------- CSV Export Callback ------------------
    # ======================================================
    @app.callback(
        Output("download-dataframe-csv", "data"),
        Input("btn_csv", "n_clicks"),
        State("filtered-data", "data"),
        prevent_initial_call=True,
    )
    def export_csv(n_clicks, data):
        if not data:
            return dash.no_update
        dff = pd.DataFrame(data)
        dff = dff[columns_to_show]
        if "order_date" in dff.columns:
            dff["order_date"] = pd.to_datetime(dff["order_date"]).dt.strftime(
                "%Y-%m-%d"
            )
        return dcc.send_data_frame(
            dff.to_csv, "filtered_swiftshop_sales.csv", index=False
        )
