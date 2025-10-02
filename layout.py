# modules/layout.py
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from modules import style
import pandas as pd

table_columns = [
    {"name": "Order Date", "id": "order_date"},
    {"name": "Customer ID", "id": "customer_id"},
    {"name": "Product", "id": "product_name"},
    {"name": "Category", "id": "category"},
    {"name": "Region", "id": "customer_region"},
    {"name": "Total Amount", "id": "total_amount"},
    {"name": "Rating", "id": "customer_rating"},
]


def create_layout(
    df,
    kpis,
    columns_to_show,
    fig_total_sales,
    fig_avg_order,
    fig_rating_dist,
    fig_category_pie,
    fig_category_sales_per_month,
    fig_rating_pie,
    fig_category_sales_pie,
):

    # ======================================================
    # ----------------- Sidebar Menu ----------------------
    # ======================================================
    sidebar = html.Div(
        [
            html.H2("SwiftShop", style=style.SIDEBAR_TITLE),
            dcc.Link("Main dashboard", href="/", style=style.SIDEBAR_LINK),
            dcc.Link("Order Details", href="/filters", style=style.SIDEBAR_LINK),
        ],
        style=style.SIDEBAR_STYLE,
    )

    # ======================================================
    # ----------------- Home Page Content -----------------
    # ======================================================
    home_content = html.Div(
        [
            # --- KPI Cards ---
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Total Sales", style=style.KPI_LABEL_STYLE),
                                html.Div(
                                    kpis["total_sales"], style=style.KPI_VALUE_STYLE
                                ),
                            ],
                            style=style.KPI_CARD_STYLE,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    "Number of Orders", style=style.KPI_LABEL_STYLE
                                ),
                                html.Div(
                                    kpis["total_orders"], style=style.KPI_VALUE_STYLE
                                ),
                            ],
                            style=style.KPI_CARD_STYLE,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div(
                                    "Average Order Value", style=style.KPI_LABEL_STYLE
                                ),
                                html.Div(
                                    kpis["avg_order_value"], style=style.KPI_VALUE_STYLE
                                ),
                            ],
                            style=style.KPI_CARD_STYLE,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div("Average Rating", style=style.KPI_LABEL_STYLE),
                                html.Div(
                                    kpis["avg_rating"], style=style.KPI_VALUE_STYLE
                                ),
                            ],
                            style=style.KPI_CARD_STYLE,
                        ),
                        width=3,
                    ),
                ],
                style=style.KPI_ROW_STYLE,
            ),
            # --- Charts ---
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            figure=fig_total_sales,
                            config=style.GRAPH_CONFIG,
                            style=style.GRAPH_STYLE,
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Graph(
                            figure=fig_avg_order,
                            config=style.GRAPH_CONFIG,
                            style=style.GRAPH_STYLE,
                        ),
                        width=6,
                    ),
                ],
                style=style.CARD_STYLE,
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(
                            figure=fig_category_sales_per_month,
                            config=style.GRAPH_CONFIG,
                            style=style.GRAPH_STYLE,
                        ),
                        width=6,
                    ),
                    dbc.Col(
                        dcc.Graph(
                            figure=fig_category_sales_pie,
                            config=style.GRAPH_CONFIG,
                            style=style.GRAPH_STYLE,
                        ),
                        width=3,
                    ),
                    dbc.Col(
                        dcc.Graph(
                            figure=fig_rating_pie,
                            config=style.GRAPH_CONFIG,
                            style=style.GRAPH_STYLE,
                        ),
                        width=3,
                    ),
                ],
                style=style.CARD_STYLE,
            ),
        ]
    )

    # ======================================================
    # ----------------- Filters Page Content -------------
    # ======================================================
    filters_content = html.Div(
        [
            html.H3("Order Details", style=style.PAGE_TITLE),
            # Filter Controls
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            "⚙️ Filters",
                            id="toggle-filters",
                            color="primary",
                            n_clicks=0,
                            className="mb-2",
                            style=style.BUTTON,
                        ),
                        width=12,
                    ),
                    dbc.Col(
                        html.Div(
                            id="filters-div",
                            children=[
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.Div(
                                                [
                                                    # ------------------- Inject inline CSS for DatePickerRange popup -------------------
                                                    html.Div(
                                                        [
                                                            html.Script(
                                                                """
                        const style = document.createElement('style');
                        style.innerHTML = `
                        .custom-date-picker .Calendar__Month { background-color: #ffebcd; color: #800000; }
                        .custom-date-picker .Calendar__Day--selected { background-color: #800000 !important; color: white !important; }
                        .custom-date-picker .Calendar__Day:hover { background-color: #ffa500; color: white; }
                        .custom-date-picker .Calendar__Navigation { background-color: #f0e68c; }
                        `;
                        document.head.appendChild(style);
                        """
                                                            )
                                                        ]
                                                    ),
                                                    # ------------------- DatePickerRange component -------------------
                                                    dcc.DatePickerRange(
                                                        id="date-picker",
                                                        min_date_allowed=df[
                                                            "order_date"
                                                        ]
                                                        .min()
                                                        .date(),
                                                        max_date_allowed=df[
                                                            "order_date"
                                                        ]
                                                        .max()
                                                        .date(),
                                                        start_date=df["order_date"]
                                                        .min()
                                                        .date(),
                                                        end_date=df["order_date"]
                                                        .max()
                                                        .date(),
                                                        display_format="YYYY-MM",
                                                        style=style.FILTER_STYLE,  # your input box style
                                                        className="custom-date-picker",  # targets the popup
                                                    ),
                                                ]
                                            ),
                                            width=3,
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="region-dropdown",
                                                multi=True,
                                                placeholder="Select Region",
                                                options=[
                                                    {"label": r, "value": r}
                                                    for r in df[
                                                        "customer_region"
                                                    ].unique()
                                                    if pd.notnull(r)
                                                ],
                                                style=style.FILTER_STYLE,
                                            ),
                                            width=4,
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id="category-dropdown",
                                                multi=True,
                                                placeholder="Select Category",
                                                options=[
                                                    {"label": c, "value": c}
                                                    for c in df["category"].unique()
                                                    if pd.notnull(c)
                                                ],
                                                style=style.FILTER_STYLE,
                                            ),
                                            width=4,
                                        ),
                                    ],
                                    style=style.FILTER_ROW,
                                )
                            ],
                            style={"display": "none"},
                        ),
                        width=12,
                    ),
                    # Main Charts + Table Row
                    dbc.Row(
                        [
                            # Left column: line chart above table
                            dbc.Col(
                                [
                                    dcc.Graph(
                                        id="sales-line",
                                        config=style.GRAPH_CONFIG,
                                        style=style.GRAPH_STYLE,
                                    ),
                                    dbc.Button(
                                        "⬇️ Export CSV",
                                        id="btn_csv",
                                        n_clicks=0,
                                        color="primary",
                                        className="my-2",
                                        style=style.BUTTON,
                                    ),
                                    dcc.Download(id="download-dataframe-csv"),
                                    dash_table.DataTable(
                                        id="orders-table",
                                        columns=table_columns,
                                        page_size=10,
                                        column_selectable="multi",
                                        style_table=style.TABLE_STYLE,
                                        style_cell=style.TABLE_CELL_STYLE,
                                        style_header=style.TABLE_HEADER_STYLE,
                                        style_data_conditional=style.TABLE_CONDITIONAL_STYLE,
                                    ),
                                ],
                                width=8,
                            ),
                            dbc.Col(
                                dcc.Graph(
                                    id="top-products",
                                    config=style.GRAPH_CONFIG,
                                    style=style.GRAPH_STYLE_VERTICAL,
                                ),
                                width=4,
                            ),
                        ],
                        style=style.CARD_STYLE,
                    ),
                ]
            ),
        ]
    )

    # ======================================================
    # ----------------- Layout: Sidebar + Content --------
    # ======================================================
    layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    sidebar,  # Left sidebar
                    html.Div(
                        id="page-content",
                        children=home_content,
                        style=style.CONTENT_STYLE,
                    ),  # Right content
                ],
                style=style.MAIN_DIV_STYLE,  # Moved inline style
            ),
            html.Div("© 2025 SwiftShop Analytics", style=style.FOOTER_STYLE),
            dcc.Store(id="filtered-data", storage_type="memory"),
        ]
    )

    # ======================================================
    # ----------------- Navigation dictionary ------------
    # ======================================================
    layout.page_dict = {"/": home_content, "/filters": filters_content}

    return layout
