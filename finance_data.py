import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set random seed for reproducibility
np.random.seed(42)

# Sample data from previous datasets
item_names = ['KH-1239', 'Cross Knob', 'Tower Bolt', 'Profile Handle', 'Key Stand', 
              'Sofa Leg', 'Main Door Handle', 'Khutti', 'Kadi Deluxe', 'Stainless Steel Knob',
              'Gold Plated Handle', 'Tower Bolt Premium', 'Economy Kadi', 'Antique Handle',
              'Designer Knob', 'Ultra Modern Handle', 'Brass Khutti', 'Decorative Kadi', 'Traditional Handle']

categories = ['Handles', 'Knob', 'Others', 'Accessories', 'Kadi']

# Generate 5000 rows of data
n_rows = 5000

# Generate dates between Oct 1, 2024 and Jan 31, 2025
start_date = datetime(2024, 10, 1)
end_date = datetime(2025, 1, 31)
dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

# Create base data
data = {
    'Finance_ID': range(10001, 10001 + n_rows),
    'Stock_ID': range(1001, 1001 + n_rows),
    'Item_Name': np.random.choice(item_names, n_rows),
    'Category': np.random.choice(categories, n_rows),
    'Date': np.random.choice(dates, n_rows)
}

df = pd.DataFrame(data)

# Generate base revenue (with some variability)
df['Revenue'] = np.random.uniform(5000, 40000, n_rows)

# Generate costs (approximately 40-60% of revenue)
cost_percentages = np.random.uniform(0.4, 0.6, n_rows)
df['Cost'] = df['Revenue'] * cost_percentages

# Add patterns and issues
# 1. Seasonal patterns (higher revenue in December)
seasonal_mask = df['Date'] >= datetime(2024, 12, 1)
df.loc[seasonal_mask & (df['Category'] == 'Handles'), 'Revenue'] *= 1.5

# 2. Category-specific patterns
df.loc[df['Category'] == 'Kadi', 'Cost'] *= 0.9  # Better margins for Kadi products
df.loc[df['Category'] == 'Accessories', 'Revenue'] *= 1.2  # Higher revenue for Accessories

# 3. Add zero revenue entries (unsold inventory)
zero_revenue_idx = np.random.choice(n_rows, 100, replace=False)
df.loc[zero_revenue_idx, 'Revenue'] = 0

# 4. Add outliers
# Extremely high revenue
revenue_outlier_idx = np.random.choice(n_rows, 30, replace=False)
df.loc[revenue_outlier_idx, 'Revenue'] *= 5

# Unusually high costs
cost_outlier_idx = np.random.choice(n_rows, 40, replace=False)
df.loc[cost_outlier_idx, 'Cost'] *= 3

# 5. Add missing values (NaN)
for column in ['Revenue', 'Cost']:
    mask = np.random.choice([True, False], size=n_rows, p=[0.02, 0.98])
    df.loc[mask, column] = np.nan

# 6. Calculate financial metrics
df['Profit'] = df['Revenue'] - df['Cost']
df['Tax'] = df['Profit'].apply(lambda x: max(0.2 * x, 0) if pd.notnull(x) and x > 0 else 0)
df['Net_Profit'] = df['Profit'] - df['Tax']

# 7. Add some incorrect/noise values
# Negative revenues (data entry errors)
noise_idx = np.random.choice(n_rows, 20, replace=False)
df.loc[noise_idx, 'Revenue'] = -df.loc[noise_idx, 'Revenue']

# Some entries with cost > revenue (loss-making transactions)
loss_making_idx = np.random.choice(n_rows, 50, replace=False)
df.loc[loss_making_idx, 'Cost'] = df.loc[loss_making_idx, 'Revenue'] * 1.2

# Sort by Date
df = df.sort_values('Date')

# Convert date to string format
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Round numerical columns to 2 decimal places
numeric_columns = ['Revenue', 'Cost', 'Profit', 'Tax', 'Net_Profit']
for col in numeric_columns:
    df[col] = df[col].round(2)

# Convert DataFrame to list of lists including headers
# Handle NaN values by converting them to 'NA'
df = df.replace({np.nan: 'NA'})
table_data = [df.columns.tolist()] + df.values.tolist()

# Convert all values to strings
table_data = [[str(cell) for cell in row] for row in table_data]

table_data


'''
    Built-in Patterns & Issues:

    Missing Values:

    2% missing values in Revenue and Cost columns (marked as 'NA')
    Corresponding Profit, Tax, and Net_Profit calculations affected
    Seasonal & Category Patterns:

    50% higher revenue for Handles category during December
    Better profit margins for Kadi products (10% lower costs)
    Higher revenue (20% increase) for Accessories
    100 zero-revenue entries representing unsold inventory
    Outliers & Errors:

    30 records with extremely high revenue (5x normal)
    40 records with unusually high costs (3x normal)
    20 records with negative revenue (data entry errors)
    50 loss-making transactions (cost > revenue)
    Financial Analysis Opportunities:

    Category-wise profitability
    Seasonal profit trends
    Tax impact analysis
    Loss-making product identification
    Stock turnover impact on finances
    The data is now in your sheet starting from cell A1. You can analyze:

    Product profitability patterns
    Seasonal financial performance
    Category-wise margin analysis
    Loss-making product investigation
    Combined analysis with inventory and sales datasets for complete stock turnover impact
'''