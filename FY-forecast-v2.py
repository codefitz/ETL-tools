import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import os

# Load the Excel file with MultiIndex columns
df = pd.read_excel(
    r'C:\Users\...\GitHub\ETL-tools\data.xlsx',
    header=[0, 1]
)

# Inspect the columns
#print("Columns in the DataFrame:")
#print(df.columns)

# Drop the unnecessary columns if they exist
columns_to_drop = [
    ('Unnamed: 0_level_0', 'Unnamed: 0_level_1')  # Adjust based on your actual needs
]

df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True)

# Set the correct 'Cluster' column as the index
if ('Unnamed: 0_level_0', 'Cluster') in df.columns:
    df.set_index(('Unnamed: 0_level_0', 'Cluster'), inplace=True)
else:
    raise KeyError("Index column ('Unnamed: 0_level_0', 'Cluster') not found in the DataFrame.")

# Flatten the columns to make it easier to work with
df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Function to prepare data for a specific cluster up to Nov of FY25
def prepare_data(cluster_name, df):
    # Filter the data up to Nov (Month 8)
    data = df.loc[cluster_name, :'FY25_Jan'].values.flatten()
    data = data[~pd.isnull(data)]  # Remove NaN values
    return data

# Forecast function with scaling based on historical average
def forecast_next_year(data, periods=14):
    if len(data) < 24:  # Ensure at least 24 months of data
        return np.array([np.nan] * periods)  # Return NaNs if not enough data
    
    # Optional smoothing (apply smoothing to reduce noise)
    data_smoothed = pd.Series(data).rolling(window=3).mean().dropna().values
    
    # Split data for cross-validation
    train_data = data_smoothed[:-periods]  # Train on smoothed data up to last 'periods' months
    test_data = data_smoothed[-periods:]  # Test on the last 'periods' months

    # Create and fit the model with multiplicative trend and additive seasonal component
    model = ExponentialSmoothing(train_data, trend='mul', seasonal='add', seasonal_periods=12)
    
    # Fit the model with default smoothing parameters
    fit = model.fit(optimized=True)

    # Forecast for the next 'periods' months
    forecast = fit.forecast(periods)

    # Calculate historical and predicted averages
    historical_avg = np.mean(train_data[-12:])  # Average of last 12 months of historical data
    forecast_avg = np.mean(forecast[:3])  # Average of forecast for first 3 months (or more if needed)

    # Calculate the scaling factor based on historical vs forecast averages
    if forecast_avg != 0:
        scaling_factor = historical_avg / forecast_avg
    else:
        scaling_factor = 1.0  # Avoid division by zero

    print(f"Historical average: {historical_avg}, Forecast average: {forecast_avg}, Scaling factor: {scaling_factor}")

    # Apply the scaling factor to the forecast
    forecast_adjusted = forecast * scaling_factor
    
    # Apply global scaling factor to increase all values by 20%
    forecast_adjusted *= 1.2

    # Ensure no negative values
    forecast_adjusted = np.maximum(forecast_adjusted, 0)

    return forecast_adjusted


# Create a DataFrame to store all forecasts
forecasts = pd.DataFrame()

# Iterate over each cluster and generate forecasts
for cluster in df.index.unique():
    print(f"Forecasting for cluster: {cluster}")
    data = prepare_data(cluster, df)
    forecast = forecast_next_year(data)
    forecasts[cluster] = forecast

# Transpose the DataFrame so that clusters are rows and months are columns
forecasts = forecasts.T
forecast_months = ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']  # Remaining months
forecasts.columns = [f'FY26_{month}' for month in forecast_months]

# Apply additional 50% reduction for FY25_Sep to FY25_Nov
#forecasts[['FY25_Dec', 'FY25_Jan', 'FY25_Mar']] *= 0.5  # 50% reduction

# Save the forecasted data to a new Excel file
output_file = r'C:\Users\...\GitHub\ETL-tools\FY25_Forecasts_from_Jan.xlsx'
forecasts.to_excel(output_file, sheet_name='FY26 Forecasts')

print(f"Forecasts successfully saved to {output_file}")
