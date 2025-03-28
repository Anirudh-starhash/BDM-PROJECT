import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Sample data from previous inventory
item_names = ['KH-1239', 'Cross Knob', 'Tower Bolt', 'Profile Handle', 'Key Stand', 
              'Sofa Leg', 'Main Door Handle', 'Khutti', 'Kadi Deluxe', 'Stainless Steel Knob',
              'Gold Plated Handle', 'Tower Bolt Premium', 'Economy Kadi', 'Antique Handle',
              'Designer Knob', 'Ultra Modern Handle', 'Brass Khutti', 'Decorative Kadi', 'Traditional Handle']

categories = ['Handles', 'Knob', 'Others', 'Accessories', 'Kadi']
regions = ['North', 'South', 'East', 'West', 'Central']

# Generate 5000 rows of data
n_rows = 5000

# Generate dates for sales (more recent than inventory dates)
start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 1, 31)
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Create base data
data = {
    'Sale_ID': range(5001, 5001 + n_rows),
    'Stock_ID': range(1001, 1001 + n_rows),
    'Item_Name': np.random.choice(item_names, n_rows),
    'Category': np.random.choice(categories, n_rows),
    'Sale_Quantity': np.random.randint(1, 50, n_rows),
    'Sale_Price': np.random.uniform(500, 3000, n_rows),
    'Discount': np.random.choice([0, 5, 10, 15, 20], n_rows),
    'Date_Sold': np.random.choice(dates, n_rows),
    'Customer_Region': np.random.choice(regions, n_rows),
    'Return_Status': np.random.choice(['No', 'Yes'], n_rows, p=[0.9, 0.1])
}

df = pd.DataFrame(data)

# Add patterns and issues
# 1. Seasonal sales patterns
seasonal_mask = df['Date_Sold'] >= datetime(2024, 12, 1)
df.loc[seasonal_mask & (df['Category'] == 'Handles'), 'Sale_Quantity'] *= 1.5

# 2. Regional preferences
df.loc[df['Customer_Region'] == 'North', 'Sale_Quantity'] *= 1.2
df.loc[df['Customer_Region'] == 'South', 'Discount'] += 5

# 3. Add zero quantity sales (cancelled orders)
zero_sales_idx = np.random.choice(n_rows, 100, replace=False)
df.loc[zero_sales_idx, 'Sale_Quantity'] = 0
df.loc[zero_sales_idx, 'Total_Revenue'] = 0

# 4. Add outliers
# Extremely high sales quantities
quantity_outlier_idx = np.random.choice(n_rows, 30, replace=False)
df.loc[quantity_outlier_idx, 'Sale_Quantity'] *= 10

# Unusually high discounts
high_discount_idx = np.random.choice(n_rows, 50, replace=False)
df.loc[high_discount_idx, 'Discount'] = 40

# 5. Add missing values (NaN)
for column in ['Sale_Quantity', 'Sale_Price', 'Discount']:
    mask = np.random.choice([True, False], size=n_rows, p=[0.02, 0.98])
    df.loc[mask, column] = np.nan

# 6. Calculate Total_Revenue with patterns
df['Total_Revenue'] = df['Sale_Quantity'] * df['Sale_Price'] * (1 - df['Discount']/100)

# 7. Add some incorrect/noise values
# Negative sales quantities (data entry errors)
noise_idx = np.random.choice(n_rows, 20, replace=False)
df.loc[noise_idx, 'Sale_Quantity'] = -df.loc[noise_idx, 'Sale_Quantity']

# Sort by Date_Sold
df = df.sort_values('Date_Sold')

# Convert date to string format
df['Date_Sold'] = df['Date_Sold'].dt.strftime('%Y-%m-%d')

# Round numerical columns
df['Sale_Price'] = df['Sale_Price'].round(2)
df['Total_Revenue'] = df['Total_Revenue'].round(2)

# Convert DataFrame to list of lists including headers
# Handle NaN values by converting them to empty strings
df = df.replace({np.nan: ''})
table_data = [df.columns.tolist()] + df.values.tolist()

# Convert all values to strings
table_data = [[str(cell) for cell in row] for row in table_data]

table_data

'''
    Built-in Patterns & Issues:

    Missing Values:

    2% missing values in Sale_Quantity, Sale_Price, and Discount columns
    Represented as empty cells
    Seasonal & Regional Patterns:

    Higher sales quantities for Handles category during December-January (50% increase)
    North region shows 20% higher sales quantities
    South region has additional 5% discounts
    100 cancelled orders (zero quantity sales)
    Outliers & Errors:

    30 records with extremely high sale quantities (10x normal)
    50 records with unusually high discounts (40%)
    20 records with impossible negative quantities
    Some inconsistent Total_Revenue calculations
    Sales Analysis Opportunities:

    Regional performance variations
    Seasonal trends
    Return rates (10% return rate built in)
    Discount impact on sales
    Stock turnover patterns when compared with inventory dataset
    The data is now in your sheet starting from cell K1. You can analyze:

    Regional sales patterns
    Seasonal demand fluctuations
    Product category performance
    Return rate analysis
    Stock turnover rates by combining with the inventory dataset
    
'''