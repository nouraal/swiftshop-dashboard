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
│   ├── app.py        # Main Dash app
│   └── data_clean.py # Data cleaning functions
├── requirements.txt  # Project dependencies
├── data/
│   └── swiftshop_sales_data.csv # Sales dataset
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
cd modules
python app.py

The app will run locally at:
http://127.0.0.1:8050/
```
### 📊 Dashboard Preview
> 1. KPIs Row 1: Total Sales Over Time, Average Order Value
> 2. KPIs Row 2: Customer Rating Distribution, Category Performance
> 3. Tabs:
>>    1. Sales Over Time (with MoM & YoY changes)
>>    2. Top 10 Products
>>    3. Orders Data (with CSV export)

###  🛠️ Technologies Used
* Python 3.10+
* Pandas
* Plotly
* Dash

* Dash Bootstrap Components
