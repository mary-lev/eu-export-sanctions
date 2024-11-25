import streamlit as st
import pandas as pd
import glob
import os
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Data Analysis", page_icon="🌍", layout="wide")

# Add sidebar
with st.sidebar:
    st.markdown('''
    ### About
    This project hypothesizes 
    that Russia is circumventing EU sanctions 
    by increasing trade through intermediary countries 
    such as Kyrgyzstan and Armenia, 
    which is reflected in anomalous trade data patterns post-2022.
    ''')

# Streamlit App for "Data Analysis"
st.title("Data Analysis")
st.write('''
### Methodology: Detecting Anomalous Trade Pattern Changes

Our analysis identified countries with unusual increases in EU export volumes using a systematic statistical approach:

#### 1. Data Collection and Preparation
- Gathered EU export data for all partner countries (2019-2023)
- Organized data to track year-over-year changes
- Focused on detecting significant changes around sanctions implementation (2021-2022)

#### 2. Statistical Analysis Process

**Step 1: Calculate Growth Rates**
- Computed year-over-year growth percentages for each country
- Example: Armenia's exports grew by 148.9% from 2021 to 2022

**Step 2: Establish Baseline**
- Used 2019-2021 as baseline period
- Calculated mean growth rate and standard deviation for each country
- This helps identify what constitutes "normal" variation

**Step 3: Detect Anomalies**
- Used Z-scores to identify statistically significant changes
- Z-score > 1.96 indicates 95% confidence that change is unusual
- Added filter for growth rates > 50% to focus on substantial changes

#### 3. Key Findings

Among the identified countries, several stand out as particularly significant:

**Primary Concerns:**
- **Kyrgyzstan**: 344.8% growth (2021-2022)
- **Armenia**: 148.9% growth (2021-2022)
- **Kazakhstan**: 88.6% growth (2021-2022)
- **Uzbekistan**: 63.8% growth (2021-2022)

These countries share important characteristics:
- Geographic proximity to Russia
- Historical economic ties with Russia
- Unprecedented growth rates
- Statistically significant deviation from historical patterns

### Significance of Findings

The identified patterns suggest systematic changes in trade flows:
- Growth rates far exceeding historical norms
- Concentration in countries neighboring Russia
- Timing coinciding with sanctions implementation
''')

# Data Processing and Visualization

# Step 1: Load and combine data files

# Use @st.cache_data to cache the data loading
@st.cache_data
def load_data():
    
    file_paths = glob.glob(os.path.join("data/eu_year_export", '*.csv'))
    dataframes = [pd.read_csv(file) for file in file_paths]
    data = pd.concat(dataframes, ignore_index=True)
    return data

data = load_data()
# Step 2: Extract year information and filter relevant data
data['YEAR'] = data['PERIOD'].str[:4].astype(int)

# Remove rows where 'YEAR' is NaN
data = data.dropna(subset=['YEAR'])
data['YEAR'] = data['YEAR'].astype(int)
MIN_EXPORT_VOLUME = 1000000000

# Step 3: Pivot the data for yearly comparison
pivot_data = data.pivot_table(
    index='PARTNER', columns='YEAR', values='VALUE_IN_EUR', aggfunc='sum'
).fillna(0)

# Step 4: Calculate year-over-year growth percentages
for year in range(2019, 2022):  # Adjust range based on your data
    if year + 1 in pivot_data.columns:
        pivot_data[f'GROWTH_{year}_{year+1}'] = ((pivot_data[year + 1] - pivot_data[year]) / pivot_data[year].replace(0, np.nan)) * 100

# Step 5: Identify statistically significant growth from 2021 to 2022
# Calculate the mean and standard deviation of previous growth rates (2019-2020 and 2020-2021)

growth_cols = [f'GROWTH_{year}_{year+1}' for year in range(2019, 2021) if f'GROWTH_{year}_{year+1}' in pivot_data.columns]
pivot_data['MEAN_PREV_GROWTH'] = pivot_data[growth_cols].mean(axis=1)
pivot_data['STD_PREV_GROWTH'] = pivot_data[growth_cols].std(axis=1)

# Calculate Z-score for the growth from 2021 to 2022
pivot_data['Z_SCORE_2021_2022'] = (pivot_data['GROWTH_2021_2022'] - pivot_data['MEAN_PREV_GROWTH']) / pivot_data['STD_PREV_GROWTH']

# MIN_EXPORT_VOLUME = st.sidebar.slider(
#     "Minimum Export Volume (EUR)", min_value=0, max_value=1000000, step=5000, value=100000
# )

# Consider growth significant if Z-score > 1.96 (95% confidence interval) and growth > 50%
significant_growth_countries = pivot_data[
    (pivot_data['Z_SCORE_2021_2022'] > 1.96) & 
    (pivot_data['GROWTH_2021_2022'] > 50) &
    (pivot_data[2022] > MIN_EXPORT_VOLUME)  # Ensure export volume in 2022 is significant
]


# Remove infinite and NaN values resulting from division by zero
significant_growth_countries = significant_growth_countries.replace([np.inf, -np.inf], np.nan).dropna(subset=['Z_SCORE_2021_2022'])

# Display the results
st.subheader("Countries with Significant Growth in Exports from EU (2021-2022)")
st.write('''
The following countries exhibited statistically significant growth in exports from the EU from 2021 to 2022 (Z-score > 1.96 and growth > 50%):
''')

# Reset index to include 'PARTNER' as a column
significant_growth_countries = significant_growth_countries.reset_index()

# Select relevant columns to display
display_columns = ['PARTNER', 2019, 2020, 2021, 2022, 'GROWTH_2019_2020', 'GROWTH_2020_2021', 'GROWTH_2021_2022', 'MEAN_PREV_GROWTH', 'STD_PREV_GROWTH', 'Z_SCORE_2021_2022']

st.dataframe(significant_growth_countries[display_columns].round(2))

# Optional: Add a visualization
st.subheader("Visualization of Export Growth Rates (2021-2022)")

# Create a bar chart of growth rates for significant countries
fig = px.bar(
    significant_growth_countries,
    x='PARTNER',
    y='GROWTH_2021_2022',
    title='Year-over-Year Export Growth Rates (2021-2022)',
    labels={'GROWTH_2021_2022': 'Growth Rate (%)', 'PARTNER': 'Country'},
    hover_data=['Z_SCORE_2021_2022']
)

st.plotly_chart(fig, use_container_width=True)
