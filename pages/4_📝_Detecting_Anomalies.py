import streamlit as st
import pandas as pd
import glob
import os
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Detecting Anomalies", page_icon="🌍", layout="wide")

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
st.title("Detecting Anomalous Trade Pattern Changes")
st.write('''Our analysis identified countries with unusual increases in EU export volumes using a systematic statistical approach:

#### **1. Data Collection and Preparation**

We began by collecting extensive EU export data for all partner countries from **2010 to 2023** from Eurostat database. 
         It contains detailed information on the value of goods exported to each country annually (columns "Partner", "Period" and "Value in EUR").
         The total amount of export for all types og goods is recorded in the column "Value in EUR".
         This rich dataset allowed us to **track long-term trends** in export volumes; **establish historical baselines** 
         for each country's trade activity and **detect deviations** that may signal significant shifts in trade relationships.

> NB. For 2016, the dataset contains different names for some countries: for example, Uzbekistan is called 'Ouzbekistan', Kyrgyzstan is called 'Kirghizistan', Armenia is called 'Arménie', and this has caused some problems in data processing,  so we need to rename these countries to their correct names in order to be consistent with data from other years.

#### **2. Data Analysis**

**1. Calculating Year-over-Year Growth Rates**. For each country, we computed the annual growth rates in export values. 
         This provided a clear picture of how trade volumes fluctuated year by year. 

**2. Detecting Historical Baselines**. The average growth rate and standard deviation for each country were calculated from 2010 to 2021. This historical baseline enabled the identification of the typical variability in trade patterns for each partner.

**3. Identifying anomalies with statistical accuracy**. Using the baseline, we calculated the **Z-score** for the growth from 2021 to 2022.
A **Z-score** quantifies how many standard deviations an element is from the mean. 
We considered a **Z-score greater than 1.96** (corresponding to a 95% confidence level) as statistically significant.
Additionally, we focused on countries with a **growth rate exceeding 50%** and an export volume greater than **100 million EUR** 
         in 2022 to ensure the changes were substantial and economically meaningful.

This analysis allows us to demonstrate with figures the real increase in trade volumes in 2022 compared to previous years:
- **Kyrgyzstan**: 344.8%
- **Armenia**: 148.9%
- **Kazakhstan**: 88.6%
- **Uzbekistan**: 63.8%
- **Trinidad and Tobago**: 122.6%

The data show a sharp increase in trade volumes with the EU in 2022, with Kyrgyzstan and Armenia leading the way. 
These trends are consistent with shifts in geopolitical and economic dynamics, particularly in the context of sanctions against Russia.

**Note**: Trinidad and Tobago also showed a remarkable increase in exports from the EU, with a growth rate of 122.6%. 
This is particularly significant given its smaller trade volumes in prior years.

#### **3. Interpreting the Patterns**

Several commonalities (geopolitical proximity, economic ties and temporal correlation) can explain these findings. 
All the countries identified are neighbours or close to Russia, facilitating potential trade diversion. 
They have established economic relations with both the EU and Russia, making them viable intermediaries. 
The timing of the export surges coincides closely with the implementation of sanctions against Russia in 2022.

So this trend analysis allows us to identify anomalies and provide a list of countries to investigate [further](/Visualization).
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
data['YEAR'] = data['PERIOD'].str[-4:].astype(int)

# Remove rows where 'YEAR' is NaN
data = data.dropna(subset=['YEAR'])
data['YEAR'] = data['YEAR'].astype(int)
MIN_EXPORT_VOLUME = 100000000

# Step 3: Pivot the data for yearly comparison
pivot_data = data.pivot_table(
    index='PARTNER', columns='YEAR', values='VALUE_IN_EUR', aggfunc='sum'
).fillna(0)

pivot_data.columns = pivot_data.columns.astype(int)

# Step 4: Calculate year-over-year growth percentages
for year in range(2010, 2023):  # Adjust range based on your data
    if year + 1 in pivot_data.columns:
        pivot_data[f'GROWTH_{year}_{year+1}'] = ((pivot_data[year + 1] - pivot_data[year]) / pivot_data[year].replace(0, np.nan)) * 100

# Step 5: Identify statistically significant growth from 2021 to 2022
# Calculate the mean and standard deviation of previous growth rates (2019-2020 and 2020-2021)
growth_cols = [f'GROWTH_{year}_{year+1}' for year in range(2010, 2021) if f'GROWTH_{year}_{year+1}' in pivot_data.columns]
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
significant_growth_countries = significant_growth_countries.sort_values('Z_SCORE_2021_2022', ascending=False)

# Display the results
st.subheader("Countries with Significant Growth in Exports from EU (2021-2022)")
st.write('''
The following countries exhibited statistically significant growth in exports from the EU from 2021 to 2022 (Z-score > 1.96 and growth > 50%):
''')

# Reset index to include 'PARTNER' as a column
significant_growth_countries = significant_growth_countries.reset_index()

# Select relevant columns to display
display_columns = ['PARTNER', 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 'GROWTH_2019_2020', 'GROWTH_2020_2021', 'GROWTH_2021_2022', 'MEAN_PREV_GROWTH', 'STD_PREV_GROWTH', 'Z_SCORE_2021_2022']

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

st.write('''
         #### **Conclusion**

So we can see that several countries, particularly **Kyrgyzstan**, **Armenia**, **Kazakhstan**, and **Uzbekistan**, have experienced significant and anomalous increases in exports from the EU in 2022. These increases are statistically significant, with Z-scores exceeding 1.96 and growth rates well above 50%, accompanied by substantial export volumes exceeding 100 million EUR.

The timing and magnitude of these trade surges, along with the geopolitical proximity and economic ties of these countries to Russia, suggest the possibility of trade redirection that may be facilitating the circumvention of EU sanctions against Russia.

These findings warrant a [deeper investigation](/Data_Analysis_and_Visualization) into the trade activities of these intermediary countries to understand the underlying factors contributing to these anomalies.
''')
