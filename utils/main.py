import streamlit as st
import pandas as pd
import math
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Country Import Volume Analysis',
    page_icon=':bar_chart:',
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def load_data():
    DATA_FILENAME = Path(__file__).parent/'data/import_volume_data.csv'
    return pd.read_csv(DATA_FILENAME, delimiter=';')

# Function to preprocess and filter data for Armenia and Kyrgyzstan
def preprocess_data_for_countries(data, countries):
    filtered_countries_data = data[data['3_variable_attribute_label'].str.contains('|'.join(countries), case=False, na=False)]
    
    # Extract the relevant data for export value and net mass for both countries
    countries_export_value = filtered_countries_data[filtered_countries_data['value_variable_label'].str.contains('Exports: Value', case=False, na=False)]
    countries_export_mass = filtered_countries_data[filtered_countries_data['value_variable_label'].str.contains('Exports: Net mass', case=False, na=False)]

    # Convert the 'time' column to a numeric type for plotting
    countries_export_value['time'] = pd.to_numeric(countries_export_value['time'], errors='coerce')
    countries_export_mass['time'] = pd.to_numeric(countries_export_mass['time'], errors='coerce')

    # Separate data for each country for better plotting
    country_data = {}
    for country in countries:
        country_data[country] = {
            'export_value': countries_export_value[countries_export_value['3_variable_attribute_label'].str.contains(country, case=False, na=False)].sort_values(by='time'),
            'export_mass': countries_export_mass[countries_export_mass['3_variable_attribute_label'].str.contains(country, case=False, na=False)].sort_values(by='time')
        }
    
    return country_data

# Function to check for significant changes after February 2022
def significant_change_analysis(data, country_name, metric_label):
    country_data = data[data['3_variable_attribute_label'].str.contains(country_name, case=False, na=False)]
    metric_data = country_data[country_data['value_variable_label'].str.contains(metric_label, case=False, na=False)]
    metric_data = metric_data.sort_values(by='time')
    
    # Split the data into pre- and post-February 2022
    pre_feb_2022 = metric_data[metric_data['time'] < 202202]['value']
    post_feb_2022 = metric_data[metric_data['time'] >= 202202]['value']
    
    # Conduct t-test to check if there is a statistically significant difference
    t_stat, p_value = stats.ttest_ind(pre_feb_2022, post_feb_2022, nan_policy='omit')
    return t_stat, p_value, pre_feb_2022, post_feb_2022

# -----------------------------------------------------------------------------
# Draw the actual page

def main():
    # Set the title that appears at the top of the page.
    st.title(':bar_chart: Country Import Volume Analysis')
    st.markdown("Browse import volume trends and analyze significant changes in data after February 2022.")
    
    # Load data from the data folder
    data = load_data()
    countries_of_interest = ["Armenia", "Kyrgyzstan", "Kazakhstan"]
    country_data = preprocess_data_for_countries(data, countries_of_interest)

    st.sidebar.title("Country and Metric Selection")
    selected_country = st.sidebar.selectbox("Select Country", countries_of_interest)
    selected_metric = st.sidebar.selectbox("Select Metric", ["Exports: Value", "Exports: Net mass"])

    # Filter the data for the selected country and metric
    if selected_metric == "Exports: Value":
        selected_country_data = country_data[selected_country]['export_value']
    elif selected_metric == "Exports: Net mass":
        selected_country_data = country_data[selected_country]['export_mass']

    # Plotting the selected metric using Streamlit's line chart for better interactivity
    if not selected_country_data.empty:
        st.header(f"{selected_metric} Trend for {selected_country} (Including Previous Years)")
        st.line_chart(selected_country_data.set_index('time')['value'])
    else:
        st.warning(f"No data available for {selected_country} and {selected_metric}")

    # Analysis of significant changes for the selected country
    t_stat, p_value, pre_feb_2022, post_feb_2022 = significant_change_analysis(data, selected_country, selected_metric)

    # Display the results
    st.subheader(f"Significant Change Analysis for {selected_country}")
    if p_value < 0.05:
        st.write(f"The change in {selected_metric} for {selected_country} after February 2022 is statistically significant (p-value = {p_value:.3f}).")
    else:
        st.write(f"No statistically significant change in {selected_metric} for {selected_country} after February 2022 (p-value = {p_value:.3f}).")

if __name__ == "__main__":
    main()
