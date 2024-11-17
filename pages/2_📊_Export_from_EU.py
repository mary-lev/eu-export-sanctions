import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px

# Set the page config
st.set_page_config(
    page_title='EU Export Analysis to Russia, Kyrgyzstan, and Armenia',
    page_icon=':bar_chart:',
    layout='wide'
)

with st.sidebar:
    st.title('Navigation')
    st.write('You are currently on: Home Page')
    
    # Optional: Add any global filters or controls
    st.subheader('Global Filters')
    time_period = st.select_slider(
        'Select Time Period',
        options=['2020', '2021', '2022', '2023', '2024'],
        value=('2020', '2024')
    )
    
    # Optional: Add other controls
    st.subheader('Data Options')
    show_raw_data = st.checkbox('Show Raw Data Tables', value=False)
    
    # Optional: Add some useful information
    st.markdown('---')  # Adds a horizontal line
    st.markdown('''
    ### About
    This project analyzes trade patterns 
    between EU and intermediary countries 
    after Russia's invasion of Ukraine.
    
    ### Data Sources
    - Eurostat
    - Kyrgyzstan Statistics
    - Russian Trade Data
    ''')

# Helper function to load data from a given folder
def load_data(folder_path):
    combined_df = pd.DataFrame()
    for file in glob.glob(os.path.join(folder_path, '*.csv')):
        df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

# Function to preprocess data
def preprocess_data(data):
    # Filter the necessary columns for visualization
    combined_df_filtered = data[['REPORTER', 'PERIOD', 'VALUE_IN_EUR']]
    
    # Remove rows where 'REPORTER' contains 'Euro area' or 'European Union'
    combined_df_filtered = combined_df_filtered[~combined_df_filtered['REPORTER'].str.contains('Euro area|European Union')]
    
    # Keep only the first word of the 'REPORTER' column
    combined_df_filtered['REPORTER'] = combined_df_filtered['REPORTER'].str.split().str[0]
    
    # Convert the 'PERIOD' column to datetime format for proper sorting
    combined_df_filtered['PERIOD'] = pd.to_datetime(combined_df_filtered['PERIOD'], format='%b. %Y')
    
    # Format 'PERIOD' to show only year and month
    combined_df_filtered['PERIOD'] = combined_df_filtered['PERIOD'].dt.strftime('%Y-%m')
    
    # Sort the data by 'PERIOD'
    combined_df_filtered = combined_df_filtered.sort_values(by='PERIOD')
    
    return combined_df_filtered

# Main function for the Streamlit page
def main():
    st.title('EU Export Analysis to Russia, Kyrgyzstan, and Armenia')

    # Load data from the three folders
    data_russia = load_data('data/russia_export_eurostat')
    data_kyrgyzstan = load_data('data/kyrgyz_export_eurostat')
    data_armenia = load_data('data/armenia_export_eurostat')

    # Create tabs for each country
    tab_russia, tab_kyrgyzstan, tab_armenia = st.tabs(['Russia', 'Kyrgyzstan', 'Armenia'])

    with tab_russia:
        combined_df_filtered = preprocess_data(data_russia)
        visualize_stacked_bar_chart(combined_df_filtered, 'Russia')

    with tab_kyrgyzstan:
        combined_df_filtered = preprocess_data(data_kyrgyzstan)
        visualize_stacked_bar_chart(combined_df_filtered, 'Kyrgyzstan')

    with tab_armenia:
        combined_df_filtered = preprocess_data(data_armenia)
        visualize_stacked_bar_chart(combined_df_filtered, 'Armenia')

# Helper function to visualize the data using Streamlit's stacked bar chart
def visualize_stacked_bar_chart(data, country_name):
    # Group data by 'REPORTER' and 'PERIOD' and sum the values for visualization
    grouped_df = data.groupby(['PERIOD', 'REPORTER'])['VALUE_IN_EUR'].sum().reset_index()
    
    if not grouped_df.empty:
        # Plotting the data using Plotly for a stacked bar chart
        fig = px.bar(
            grouped_df,
            x='PERIOD',
            y='VALUE_IN_EUR',
            color='REPORTER',
            title=f'Exports to {country_name} from EU Countries (2019 - 2024)',
            labels={'VALUE_IN_EUR': 'Value in EUR', 'PERIOD': 'Month', 'REPORTER': 'Country'},
        )
        fig.update_layout(barmode='stack', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for exports to {country_name}")

if __name__ == "__main__":
    main()
