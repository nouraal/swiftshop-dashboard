# SwiftShop Sales Dashboard 📊

An **interactive sales analytics dashboard** built with [Dash](https://dash.plotly.com/), [Plotly](https://plotly.com/python/), and [Pandas](https://pandas.pydata.org/).  
The dashboard provides **KPIs, charts, and filters** to explore SwiftShop sales data.

---

## 🚀 Features

- Data Cleaning with `data_clean.py`:
  - Fill missing customer ratings using product-level mode
  - Fill missing customer regions using customer-level mode
  - Standardize dates and extract Year/Month/Month Name
  - Handle missing payment methods and customer regions

- Dashboard with `app.py`:
  - Total sales over time (with MoM & YoY changes)
  - Average order value over time
  - Customer rating distribution
  - Product category performance (pie chart)
  - Top 10 products by sales
  - Interactive filters:
    - Date range
    - Region
    - Category
  - Data table with export to CSV

---

## 📂 Project Structure

project/
│
├── modules/
│   ├── style.py             # Styling functions and definitions
│   ├── layout.py            # Layout components for the dashboard
│   ├── kpi_calculations.py  # Functions to calculate KPIs
│   ├── data_load.py         # Functions to load data
│   ├── data_clean.py        # Data cleaning functions
│   ├── charts.py            # Chart generation functions
│   └── callbacks.py         # Callbacks for interactive elements
│
├── data/
│   └── swiftshop_sales_data.csv # Sales dataset
│
├── assets/
│   └── styles.css          # CSS styles for the dashboard
│
└── app.py               # Main application entry point
├── requirements.txt  # Project dependencies
└── README.md         # Project documentation

---

## ⚙️ Installation

### 1. Clone the repository
```
git clone https://github.com/nouraal/swiftshop-dashboard.git
cd swiftshop-dashboard
```
### 2. Create virtual environment
```
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### ▶️ Run the App
```
python app.py

The app will run locally at:
http://127.0.0.1:8050/
```
### 📊 Dashboard Preview
>The dashboard includes a sleek side menu for easy navigation between pages, and it has two main pages:

> Main Dashboard Page:
>> Top Section: Displays key metrics such as Total Sales, Number of Orders, Average Order Value, and Average Rate.
>> Charts: Visual representations of sales data and other key performance indicators.
> Order Details Page:
>> Charts: Detailed visualizations of order data.
>> Data Table: A comprehensive table listing order details.
>> Filters: Interactive filters to refine the displayed data based on various parameters.

###  🛠️ Technologies Used
* Python 3.10+
* Pandas
* Plotly
* Dash

* Dash Bootstrap Components


