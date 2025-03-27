import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

# Load the timesheet data
file_path = r'C:\Users\86011919\...\GitHub\ETL-tools\\timesheets.xlsx'
df = pd.read_excel(file_path)

# Convert the 'Row Labels' column to datetime by extracting the start date of the range
df['Row Labels'] = pd.to_datetime(df['Row Labels'].apply(lambda x: x.split(' - ')[0]), format='%d/%m/%Y')

# Rename 'Row Labels' to 'Weeks' for consistency
df.rename(columns={'Row Labels': 'Weeks'}, inplace=True)

# Prepare a list of future weeks from 01/09/2024 to the end of March 2025
future_dates = pd.date_range(start='2025-01-05', end='2025-03-31', freq='W-MON')

# Function to predict future values using linear regression
def predict_timesheet(data):
    # Prepare the data for linear regression
    data = data.dropna()
    X = np.array((data.index - data.index[0]).days).reshape(-1, 1)
    y = data.values

    # Fit the model
    model = LinearRegression()
    model.fit(X, y)

    # Predict the future dates
    future_X = np.array((future_dates - data.index[0]).days).reshape(-1, 1)
    future_y = model.predict(future_X)

    # Ensure no negative values
    future_y = np.maximum(future_y, 0)

    return future_y

# Apply the prediction for each person
predictions = {}
for person in df.columns[1:]:  # Exclude the 'Weeks' column
    df_person = df.set_index('Weeks')[person]
    predictions[person] = predict_timesheet(df_person)

# Create a DataFrame for the predictions
predicted_df = pd.DataFrame(predictions, index=future_dates)

# Calculate the grand total for the predicted weeks
predicted_df['Grand Total'] = predicted_df.sum(axis=1)

# Save the predictions to a new Excel file
output_file = r'C:\Users\86011919\...\GitHub\ETL-tools\\predicted_timesheets.xlsx'
predicted_df.to_excel(output_file)

print(f"Predictions saved to {output_file}")
