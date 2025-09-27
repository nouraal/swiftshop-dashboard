# --- Import pandas for data analysis ---
import pandas as pd

def clean(df):
    # --- Quick checks on dataset structure ---
    #df.shape          # Shows number of rows and columns
    #df.info()         # Shows column names, data types, and non-null counts
    #df.isnull().sum() # Shows count of missing values for each column


    # =====================================================================
    # --- Handling Missing Values ---
    # =====================================================================

    # --- Fill missing values in customer_rating ---
    # Step 1: For each product_id, find the most frequent (mode) rating
    product_rating_map = df.groupby('product_id')['customer_rating'] \
        .apply(lambda x: x.dropna().mode()[0] if not x.dropna().empty else None)

    # Step 2: Replace missing ratings with the mode value for that product_id
    df['customer_rating'] = df.apply(
        lambda row: product_rating_map[row['product_id']]
        if pd.isna(row['customer_rating']) else row['customer_rating'],
        axis=1
    )

    # Step 3: Convert customer_rating column to integers (ratings should be whole numbers)
    df['customer_rating'] = df['customer_rating'].astype(int)


    # --- Fill missing values in customer_region ---
    # Step 1: For each customer_id, find the most frequent (mode) region
    customer_region_map = df.groupby('customer_id')['customer_region'] \
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)

    # Step 2: Replace missing region values using the mode region for that customer_id
    df['customer_region'] = df.apply(
        lambda row: customer_region_map[row['customer_id']]
        if pd.isna(row['customer_region']) else row['customer_region'],
        axis=1
    )


    # =====================================================================
    # --- Date Handling ---
    # =====================================================================

    # 1. Convert order_date column to datetime format (invalid entries → NaT)
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # 2. Extract new time-based columns from order_date
    df["year"] = df["order_date"].dt.year        # Year as number (e.g., 2024)
    df["month"] = df["order_date"].dt.month      # Month as number (1–12)
    df["month_name"] = df["order_date"].dt.strftime("%B")  # Month name (e.g., January)


    # =====================================================================
    # --- Fill Remaining Missing Values ---
    # =====================================================================

    # Replace missing customer_region with "Unknown Region"
    df["customer_region"] = df["customer_region"].fillna("Unknown Region")

    # Replace missing payment_method with "Unknown"
    df["payment_method"] = df["payment_method"].fillna("Unknown")


    # =====================================================================
    # --- Final Dataset Checks ---
    # =====================================================================

    # 1. Verify dataset info (columns, datatypes, null counts)
    #df.info()

    # 2. Verify that no missing values remain after cleaning
    #df.isnull().sum()

    # 3. Preview the first few rows of the cleaned dataset
    #df.head()

    # 4. Generate descriptive statistics 
    #    (mean, std, min, max, quartiles) for numeric columns
    #df.describe()
    return df