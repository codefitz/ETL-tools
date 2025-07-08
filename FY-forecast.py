import argparse
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

parser = argparse.ArgumentParser(description="Generate FY25 forecasts")
parser.add_argument("--data", required=True, help="Path to input Excel file")
parser.add_argument("--output", required=True, help="Path for the output Excel file")
args = parser.parse_args()

# Load the Excel file with MultiIndex columns
df = pd.read_excel(args.data, header=[0, 1])

# Drop any unnecessary unnamed columns
df.drop(columns=[('Unnamed: 0_level_0', 'Unnamed: 0_level_1')], inplace=True)

# Set 'Cluster' as the index
df.set_index(('Unnamed: 1_level_0', 'Cluster'), inplace=True)

# Flatten the columns to make it easier to work with
df.columns = ['_'.join(col).strip() for col in df.columns.values]

# Check the DataFrame structure
print(df.head())

# Function to prepare data for a specific cluster up to July of FY25
def prepare_data(cluster_name, df):
    # Filter the data up to July (Month 4)
    data = df.loc[cluster_name, :'FY25_Jul'].values.flatten()
    data = data[~pd.isnull(data)]  # Remove NaN values
    return data

# Modified forecast function with adjustments
def forecast_next_year(data, periods=8):
    if len(data) < 24:  # Ensure at least 24 months of data
        return np.array([np.nan] * periods)  # Return NaNs if not enough data
    
    # Optional smoothing (apply smoothing to reduce noise)
    data_smoothed = pd.Series(data).rolling(window=3).mean().dropna().values
    
    # Split data for cross-validation
    train_data = data_smoothed[:-periods]  # Train on smoothed data up to last 'periods' months
    test_data = data_smoothed[-periods:]  # Test on the last 'periods' months

    # Create and fit the model with multiplicative trend and additive seasonal component (without damping for now)
    model = ExponentialSmoothing(train_data, trend='mul', seasonal='add', seasonal_periods=12)
    
    # Fit the model with updated smoothing parameters
    fit = model.fit(smoothing_level=0.2, smoothing_trend=0.1, smoothing_seasonal=0.2, optimized=False)
    
    # Forecast for the next 'periods' months
    forecast = fit.forecast(periods)
    
    # Cap values at the 95th percentile of training data to avoid spikes
    forecast = np.minimum(forecast, np.percentile(train_data, 95))

    # Apply scaling: reduce all forecast values by 50%
    forecast *= 0.5

    # Return the forecast
    return forecast

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
forecast_months = ['Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar']  # Remaining months of FY25
forecasts.columns = [f'FY25_{month}' for month in forecast_months]

# Apply additional 60% reduction for FY25_Sep to FY25_Nov
forecasts[['FY25_Sep', 'FY25_Oct', 'FY25_Nov']] *= 0.4  # 60% reduction

# Save the forecasted data to a new Excel file
output_file = args.output
forecasts.to_excel(output_file, sheet_name='FY25 Forecasts')

print(f"Forecasts successfully saved to {output_file}")
