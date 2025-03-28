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
    'Operation_ID': range(20001, 20001 + n_rows),
    'Stock_ID': range(1001, 1001 + n_rows),
    'Item_Name': np.random.choice(item_names, n_rows),
    'Category': np.random.choice(categories, n_rows),
    'Date': np.random.choice(dates, n_rows)
}

df = pd.DataFrame(data)

# Generate base operational metrics
df['Orders_Processed'] = np.random.randint(20, 200, n_rows)
df['Employee_Efficiency_Percentage'] = np.random.uniform(70, 95, n_rows)
df['Machine_Downtime_Hours'] = np.random.uniform(2, 15, n_rows)

# Calculate related metrics
df['Delayed_Orders'] = (df['Orders_Processed'] * np.random.uniform(0.05, 0.15, n_rows)).astype(int)
df['Returned_Orders'] = (df['Orders_Processed'] * np.random.uniform(0.02, 0.08, n_rows)).astype(int)

# Add patterns and issues
# 1. Seasonal patterns (December holiday rush)
seasonal_mask = df['Date'] >= datetime(2024, 12, 1)
df.loc[seasonal_mask, 'Orders_Processed'] *= 1.4
df.loc[seasonal_mask, 'Machine_Downtime_Hours'] *= 1.3
df.loc[seasonal_mask, 'Employee_Efficiency_Percentage'] *= 0.9

# 2. Category-specific patterns
# Handles have more processing issues
df.loc[df['Category'] == 'Handles', 'Machine_Downtime_Hours'] *= 1.5
df.loc[df['Category'] == 'Handles', 'Employee_Efficiency_Percentage'] *= 0.9

# Kadi products are more efficient
df.loc[df['Category'] == 'Kadi', 'Machine_Downtime_Hours'] *= 0.7
df.loc[df['Category'] == 'Kadi', 'Employee_Efficiency_Percentage'] *= 1.1

# 3. Add zero-operation days (complete shutdowns)
shutdown_idx = np.random.choice(n_rows, 50, replace=False)
df.loc[shutdown_idx, ['Orders_Processed', 'Delayed_Orders', 'Returned_Orders']] = 0
df.loc[shutdown_idx, 'Employee_Efficiency_Percentage'] = 0
df.loc[shutdown_idx, 'Machine_Downtime_Hours'] = 24

# 4. Add outliers
# Extremely high orders
order_outlier_idx = np.random.choice(n_rows, 30, replace=False)
df.loc[order_outlier_idx, 'Orders_Processed'] *= 5

# Severe efficiency issues
efficiency_outlier_idx = np.random.choice(n_rows, 40, replace=False)
df.loc[efficiency_outlier_idx, 'Employee_Efficiency_Percentage'] *= 0.4

# Extended downtime
downtime_outlier_idx = np.random.choice(n_rows, 25, replace=False)
df.loc[downtime_outlier_idx, 'Machine_Downtime_Hours'] *= 4

# 5. Add missing values (NaN)
for column in ['Orders_Processed', 'Machine_Downtime_Hours', 'Employee_Efficiency_Percentage']:
    mask = np.random.choice([True, False], size=n_rows, p=[0.02, 0.98])
    df.loc[mask, column] = np.nan

# 6. Add some incorrect/noise values
# Impossible efficiency percentages
noise_idx = np.random.choice(n_rows, 15, replace=False)
df.loc[noise_idx, 'Employee_Efficiency_Percentage'] = np.random.uniform(100, 120, 15)

# Negative orders (data entry errors)
neg_orders_idx = np.random.choice(n_rows, 20, replace=False)
df.loc[neg_orders_idx, 'Orders_Processed'] = -df.loc[neg_orders_idx, 'Orders_Processed']

# More returns than orders (logical errors)
return_error_idx = np.random.choice(n_rows, 10, replace=False)
df.loc[return_error_idx, 'Returned_Orders'] = df.loc[return_error_idx, 'Orders_Processed'] * 1.2

# Sort by Date
df = df.sort_values('Date')

# Convert date to string format
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

# Round numerical columns
df['Employee_Efficiency_Percentage'] = df['Employee_Efficiency_Percentage'].round(1)
df['Machine_Downtime_Hours'] = df['Machine_Downtime_Hours'].round(1)

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

    2% missing values in Orders_Processed, Machine_Downtime_Hours, and Employee_Efficiency_Percentage (marked as 'NA')
    Random distribution across all dates and categories
    Seasonal & Category Patterns:

    December holiday rush effects:
    40% increase in Orders_Processed
    30% increase in Machine_Downtime_Hours
    10% decrease in Employee_Efficiency
    Category-specific issues:
    Handles: 50% more downtime, 10% lower efficiency
    Kadi products: 30% less downtime, 10% higher efficiency
    50 complete shutdown days (zero operations)
    Outliers & Errors:

    30 records with extremely high orders (5x normal)
    40 records with severe efficiency issues (60% below normal)
    25 records with extended downtime (4x normal)
    15 records with impossible efficiency (>100%)
    20 records with negative orders
    10 records with more returns than orders
    Operational Analysis Opportunities:

    Machine downtime impact on order processing
    Employee efficiency correlation with delays
    Category-wise operational performance
    Return rate patterns
    Seasonal operational challenges
    The data is now in your sheet starting from cell A1. You can analyze:

    Operational efficiency patterns
    Processing bottlenecks
    Category-wise performance issues
    Impact of downtime on stock turnover
    Combined analysis with inventory, sales, and finance datasets
'''