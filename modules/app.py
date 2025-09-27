# ======================================================
# ----------------- Import Libraries  ------------------
# ======================================================
import dash
from dash import dcc, html, Input, Output, State, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import data_clean



# ======================================================
# --------------- Load / Prepare Data  -----------------
# ======================================================
# --- Load the dataset from CSV file ---
df = pd.read_csv("data/swiftshop_sales_data.csv")
df = data_clean.clean(df)

# --- 1. Remove Columns for DataTable and CSV export ---
columns_to_exclude = ["year", "month", "month_name", "period"]
columns_to_show = [col for col in df.columns if col not in columns_to_exclude]


# ======================================================
# ----------------- KPI Calculations  ------------------
# ======================================================

# 1. Total Sales
total_sales = df['total_amount'].sum()

# 2. Average Order Value
avg_order_daily = df.groupby('order_date', as_index=False)['total_amount'].mean()
average_order_value = df['total_amount'].mean()

# 3. Sales Over Time
sales_over_time = df.groupby('order_date', as_index=False)['total_amount'].sum()

# 4. Sales by Region
sales_by_region = df.groupby('customer_region', as_index=False)['total_amount'].sum()

# 5. Sales by Category
sales_by_category = df.groupby('category', as_index=False)['total_amount'].sum()

# 6. Average Customer Rating per Region
avg_rating_region = df.groupby('customer_region', as_index=False)['customer_rating'].mean()

# 7. Orders by Payment Method
orders_by_payment = df['payment_method'].value_counts().reset_index()
orders_by_payment.columns = ['payment_method', 'count']

# 8. Top 10 Products by Sales
top_products = df.groupby('product_name', as_index=False)['total_amount'].sum().sort_values('total_amount', ascending=False).head(10)

# 9. Average Customer Rating
avg_customer_rating = df['customer_rating'].mean() if 'customer_rating' in df.columns else None

# ======================================================
# --------------- Create KPI Charts --------------------
# ======================================================

# 1. Total Sales Over Time
fig_total_sales = px.line(
    sales_over_time,
    x='order_date',
    y='total_amount',
    title='Total Sales Over Time',
    markers=True,
    labels={'order_date': 'Date', 'total_amount': 'Total Sales'},
    hover_data={'total_amount': ':,.0f'}
)
fig_total_sales.update_layout(yaxis=dict(title='', showticklabels=True))

# 2. Average Order Value Over Time
fig_avg_order = px.line(
    avg_order_daily,
    x='order_date',
    y='total_amount',
    title='Average Order Value Over Time',
    markers=True,
    labels={'order_date': 'Date', 'total_amount': 'Average Order Value'},
    hover_data={'total_amount': ':,.0f'}
)
fig_avg_order.update_layout(yaxis=dict(title='', showticklabels=True))

# 3. Customer Rating Distribution
fig_rating_dist = px.histogram(
    df,
    x='customer_rating', 
    nbins=5,
    title='Customer Rating',
    labels={'customer_rating': 'Customer Rating', 'count': 'Number of Orders'},
    color='customer_rating'
)

# 4. Category Performance
fig_category_pie = px.pie(
    sales_by_category,
    names='category',
    values='total_amount',
    title='Product Category Performance',
    hover_data={'total_amount': ':,.0f'}, 
    labels={'total_amount': 'Total Sales'}
)

# ======================================================
# -------------------- Dash app ------------------------
# ======================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

columns_to_exclude = ["year", "month", "month_name", "period"]
columns_to_show = [col for col in df.columns if col not in columns_to_exclude]

# ======================================================
# ---------------------- Layout ------------------------
# ======================================================
app.layout = html.Div([
    # Header 1 - KPI
    html.H1("Key Performance Indicator", style={'textAlign': 'center', 'marginBottom': 20}),

    # KPI Row 1 - first 2 charts
    dbc.Row([
    dbc.Col(dcc.Graph(figure=fig_total_sales), width=6),
    dbc.Col(dcc.Graph(figure=fig_avg_order), width=6),
    ], style={'marginBottom': 20}),

    # KPI Row 2 - next 2 charts
    dbc.Row([
    dbc.Col(dcc.Graph(figure=fig_rating_dist), width=6),
    dbc.Col(dcc.Graph(figure=fig_category_pie), width=6),
    ], style={'marginBottom': 30}),

    # Header 2 - Dashboard Filters
    html.H1("Sales Dashboard with Filters", style={'textAlign': 'center', 'marginBottom': 20}),

    # Filters
    dbc.Row([
        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=df['order_date'].min(),
                max_date_allowed=df['order_date'].max(),
                start_date=df['order_date'].min(),
                end_date=df['order_date'].max(),
                display_format='YYYY-MM'
            )
        ], width=4),

        dbc.Col([
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in df['customer_region'].unique()],
                placeholder="Select Customer Region",
                multi=True,
                style={'height': '48px', 'fontSize': '18px'}
            )
        ], width=4),
        dbc.Col([
            dcc.Dropdown(
                id='category-dropdown',
                options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
                placeholder="Select Product Category",
                multi=True,
                style={'height': '48px', 'fontSize': '18px'}
            )
        ], width=4)
    ], style={'marginBottom': 20}),


    # Tabs for charts and table
    dcc.Tabs([
        dcc.Tab(label='Sales Over Time', children=[
            dcc.Graph(id='sales-line')
        ]),
        dcc.Tab(label='Top 10 Products', children=[
            dcc.Graph(id='top-products')
        ]),
        dcc.Tab(
        label='Orders Data',
        children=[
                dbc.Button(
            "⬇️ Export CSV",
            id="btn_csv",
            n_clicks=0,
            color="primary",
            className="my-2"
        ),
        dcc.Download(id="download-dataframe-csv"),
        dash_table.DataTable(
            id='orders-table',
            columns=[{"name": i, "id": i} for i in columns_to_show],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'}
        )
        ]
        )
    ]),

    # Store for filtered data (for CSV)
    dcc.Store(id="filtered-data", storage_type="memory")
])

# ======================================================
# ------------ Callback to update chart ----------------
# ======================================================
# --- Callback to Filters ---
@app.callback(
    Output('sales-line', 'figure'),
    Output('top-products', 'figure'),
    Output('orders-table', 'data'),
    Output('filtered-data', 'data'), 
    Input('date-picker', 'start_date'),
    Input('date-picker', 'end_date'),
    Input('region-dropdown', 'value'),
    Input('category-dropdown', 'value')
)
def update_dashboard(start_date, end_date, selected_regions, selected_categories):
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)


# ======================================================
# ------------------ Filters checks --------------------
# ======================================================
    # Filter by date
    filtered_df = df[
        ((df['year'] > start_date.year) | ((df['year'] == start_date.year) & (df['month'] >= start_date.month))) &
        ((df['year'] < end_date.year) | ((df['year'] == end_date.year) & (df['month'] <= end_date.month)))
    ]

    # Filter by region if selected
    if selected_regions:
        filtered_df = filtered_df[filtered_df['customer_region'].isin(selected_regions)]

    # Filter by category if selected
    if selected_categories:
        filtered_df = filtered_df[filtered_df['category'].isin(selected_categories)]

    
# ======================================================
# ---------- ِAdd MoM & YoY  to Line Chart---------------
# ======================================================
    # Aggregate total sales by month
    sales_over_time = filtered_df.groupby(['year', 'month'], as_index=False)['total_amount'].sum()
    sales_over_time['period'] = sales_over_time['year'].astype(str) + "-" + sales_over_time['month'].astype(str)

    # Calculate MoM & YoY
    sales_over_time['MoM_change'] = sales_over_time['total_amount'].pct_change() * 100
    sales_over_time['YoY_change'] = sales_over_time['total_amount'].pct_change(12) * 100


    # Create line chart
    fig_line = px.line(
        sales_over_time,
        x='period',
        y='total_amount',
        title='Total Sales Over Time',
        markers=True,
        labels={'period': 'Year-Month', 'total_amount': 'Total Sales'},
        hover_data={'total_amount': ':,.2f'}    
    )

    # Add MoM line
    fig_line.add_scatter(
        x=sales_over_time['period'], 
        y=sales_over_time['MoM_change'],
        mode='lines+markers', 
        name='Month over Month Change',
        hovertemplate='%{y:.2f}%<extra></extra>' 
    )
    
    # Add YoY line
    fig_line.add_scatter(
        x=sales_over_time['period'], 
        y=sales_over_time['YoY_change'],
        mode='lines+markers', 
        name='Year over Year Change',
        hovertemplate='%{y:.2f}%<extra></extra>'
    )

# ======================================================
# ---------- ِTop 10 Products Chart (Bar) ---------------
# ======================================================
    # --- Top 10 Products by Sales ---
    top_products = filtered_df.groupby('product_name', as_index=False)['total_amount'].sum()
    top_products = top_products.sort_values(by='total_amount', ascending=False).head(10)

    fig_top = px.bar(
        top_products,
        x='product_name',
        y='total_amount',
        title='Top 10 Products by Sales',
        labels={'product_name': 'Product', 'total_amount': 'Total Sales'},
        hover_data={'total_amount': ':,.2f'}
    )

# ======================================================
# -------------------- ِData Frame ----------------------
# ======================================================
    # Format the text to include commas and two decimals
    fig_top.update_traces(
    text=top_products['total_amount'].astype(int),
    texttemplate='%{text:,}', 
    textposition='outside'
    )

    # Add some extra space above the highest bar so the number above the bar will be fully appear
    fig_top.update_layout(
    yaxis=dict(range=[0, top_products['total_amount'].max() * 1.15])  # 15% extra
    )

    # Format order_date for DataTable (remove time)
    filtered_table_df = filtered_df[columns_to_show].copy()
    if 'order_date' in filtered_table_df.columns:
        filtered_table_df['order_date'] = pd.to_datetime(filtered_table_df['order_date']).dt.strftime("%Y-%m-%d")

    return fig_line, fig_top, filtered_table_df.to_dict('records'), filtered_df.to_dict('records')

# --- Callback to export CSV ---
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State("filtered-data", "data"),
    prevent_initial_call=True
)
def export_csv(n_clicks, data):
    if not data:
        return dash.no_update
    dff = pd.DataFrame(data)
    dff = dff[columns_to_show]
    if 'order_date' in dff.columns:
        dff['order_date'] = pd.to_datetime(dff['order_date']).dt.strftime("%Y-%m-%d")
    return dcc.send_data_frame(dff.to_csv, "filtered_swiftshop_sales.csv", index=False)
    
# ======================================================
# ------------------- Run server -----------------------
# ======================================================
if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)

