import pandas as pd

# Load the Excel file
file_path = 'data/kyrgyzstan_data/4.03.00.20 Географическое распределение импорта товаров..xlsx'


# Load the data from the first sheet
xl = pd.ExcelFile(file_path)
sheet_name = xl.sheet_names[0]
df = xl.parse(sheet_name, header=None)

# Identify the actual data start - typically we want the first row with meaningful data
# Drop irrelevant rows manually based on visual inspection
# Assuming data starts from row 2 or index 2 in this case:
df = df.iloc[2:, :]

# Rename the columns to make them easier to work with
columns = ['Category'] + [str(year) for year in range(1994, 2024)]
df.columns = columns[:len(df.columns)]

# Drop any empty or irrelevant columns at the end if present
df = df.loc[:, ~df.columns.duplicated()]

# Filter rows to focus on relevant categories ('Total' and 'The EU')
filtered_data = df[df['Category'].isin(['Бардыгы', 'ЕС'])]

# Clean up the data: remove commas and non-breaking spaces
for col in filtered_data.columns[1:]:
    filtered_data[col] = pd.to_numeric(
        filtered_data[col].astype(str).str.replace(',', '').str.replace('\xa0', ''),
        errors='coerce'
    )

# Reshape the DataFrame for visualization
melted_df = filtered_data.melt(id_vars=['Category'], var_name='Year', value_name='Value')
melted_df['Year'] = melted_df['Year'].astype(int)

# Display the cleaned data (or save it for use in your Streamlit app)
print(melted_df.head())

# Optional: Save to CSV for use in Streamlit
melted_df.to_csv('cleaned_kyrgyzstan_state_statistics.csv', index=False)
