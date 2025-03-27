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
def forecast_next_year_with_mse(data, cluster_name=None, periods=14):
    """
    Forecast the next 'periods' points using simple (no seasonality) Exponential Smoothing,
    optionally with a damped additive trend.
    """
    if len(data) < (12 + periods):
        return np.array([np.nan] * periods), np.nan

    # 1. Train/test split
    train_data = data[:-periods]
    test_data = data[-periods:]

    # 2. Build the model
    #    - No seasonality: seasonal=None (and remove seasonal_periods).
    #    - Additive trend with damped_trend=True can help prevent runaway forecasts.
    model = ExponentialSmoothing(
        train_data,
        trend='add',        # or 'add' for a simple upward/downward trend
        damped_trend=True,  # set to False if you don't want damping
        seasonal=None       # remove seasonality entirely
    )

    # 3. Fit on train_data
    fit = model.fit(optimized=True)
    forecast_test = fit.forecast(periods)
    
    # 4. Calculate MSE on test portion
    mse = mean_squared_error(test_data, forecast_test)

    # 5. Refit on the entire dataset for the final forecast
    model_full = ExponentialSmoothing(
        data, 
        trend='add',
        damped_trend=True,
        seasonal=None
    )
    fit_full = model_full.fit(optimized=True)
    forecast_final = fit_full.forecast(periods)

    # 6. (Optional) Clamp or scale
    #    - If your forecasts are still too high, you can multiply by e.g. 0.7 to scale them down by 30%.
    #    - If METAR should not be below ~2k, clamp that up.
    if cluster_name == "METAR":
        forecast_final = np.maximum(forecast_final, 2000)
    else:
        forecast_final = np.maximum(forecast_final, 0)

    #    - Example: scale all clusters down by 30% if you consistently see higher than real
    # forecast_final = forecast_final * 0.7

    return forecast_final, mse

forecasts = pd.DataFrame()
mse_dict = {}

for cluster in df.index.unique():
    data = prepare_data(cluster, df)
    
    # Pass cluster name so you can apply cluster-specific logic if you want:
    forecast, mse_value = forecast_next_year_with_mse(data, cluster_name=cluster)
    
    forecasts[cluster] = forecast
    mse_dict[cluster] = mse_value

# Transpose, rename columns, and save as usual
forecasts = forecasts.T
forecast_months = ['Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar']
forecasts.columns = [f'FY26_{m}' for m in forecast_months]

output_file = r'C:\Users\...\GitHub\ETL-tools\FY25_Forecasts_from_Jan.xlsx'
forecasts.to_excel(output_file, sheet_name='FY26 Forecasts')

for cluster, mse_val in mse_dict.items():
    print(f"{cluster}: MSE={mse_val}")


