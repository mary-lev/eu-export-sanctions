import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Export Dashboard',
    page_icon=':earth_americas:',  # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_export_data():
    """Load export data from a CSV file."""
    DATA_FILENAME = Path(__file__).parent/'data/import_volume_data.csv'
    raw_export_df = pd.read_csv(DATA_FILENAME, delimiter=';')

    # Filter data for Russia, Armenia, Kazakhstan only
    export_data_filtered = raw_export_df[raw_export_df['3_variable_attribute_label'].str.contains(
        'Russia|Armenia|Kazakhstan', case=False, na=False)]
    
    # Create a datetime column from year and month
    export_data_filtered['datetime'] = pd.to_datetime(
    export_data_filtered['time'].astype(str) + ' ' + export_data_filtered['1_variable_attribute_label'],
    format='%Y %B',
    errors='coerce'
)

    # Drop rows with NaT in 'datetime' after conversion to avoid issues
    export_data_filtered = export_data_filtered.dropna(subset=['datetime'])

    # Filter to include only relevant value types (Exports: Value, Exports: Net mass)
    export_data_filtered = export_data_filtered[export_data_filtered['value_variable_label'].str.contains(
    'Exports: Value \(US-Dollar\)', case=False, na=False)]

    # Select relevant columns for easier processing
    export_data_filtered = export_data_filtered[['3_variable_attribute_label', 'datetime', 'value_variable_label', 'value']]
    export_data_filtered.rename(columns={'3_variable_attribute_label': 'country', 'value_variable_label': 'export_type'}, inplace=True)

    # Convert value to numeric
    export_data_filtered['value'] = pd.to_numeric(export_data_filtered['value'], errors='coerce')

    return export_data_filtered

export_data = get_export_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: Export Dashboard

Explore Germany's export data to Russia, Armenia, and Kazakhstan from 2010 to 2024.
'''

# Add some spacing
''
''

# Ensure there is valid data before proceeding
if not export_data.empty:
    min_year = int(export_data['datetime'].min().year)
    max_year = int(export_data['datetime'].max().year)

    from_year, to_year = st.slider(
        'Which years are you interested in?',
        min_value=min_year,
        max_value=max_year,
        value=[min_year, max_year],
        step=1
    )
else:
    st.warning('No data available to determine the year range.')
    from_year, to_year = None, None

countries = ['Russia', 'Armenia', 'Kazakhstan']

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['Russia', 'Armenia', 'Kazakhstan']
)

# Filter the data
if from_year is not None and to_year is not None:
    filtered_export_data = export_data[
        (export_data['country'].str.contains('|'.join(selected_countries), case=False, na=False))
        & (export_data['datetime'].dt.year <= to_year)
        & (from_year <= export_data['datetime'].dt.year)
    ]
else:
    filtered_export_data = pd.DataFrame()

# Draw charts if there's data available
if not filtered_export_data.empty:
    st.header('Export Data over Time', divider='gray')

    # Line charts for Export Value and Mass
    for export_type in filtered_export_data['export_type'].unique():
        st.subheader(f'{export_type} Over Time')
        export_type_data = filtered_export_data[filtered_export_data['export_type'] == export_type]
        st.line_chart(
            export_type_data.set_index('datetime').pivot(columns='country', values='value'),
            use_container_width=True
        )
else:
    st.warning('No export data available for the selected filters.')

''
''

# Display Metrics for Selected Countries in Selected Year Range
if not filtered_export_data.empty:
    st.header(f'Export Metrics from {from_year} to {to_year}', divider='gray')

    cols = st.columns(len(selected_countries))

    for i, country in enumerate(selected_countries):
        col = cols[i % len(cols)]

        with col:
            country_data = filtered_export_data[filtered_export_data['country'].str.contains(country, case=False, na=False)]
            total_value_usd = country_data['value'].sum() / 1e6  # Convert to millions

            if not country_data.empty:
                st.metric(
                    label=f'{country} Export Value (M USD)',
                    value=f'{total_value_usd:,.2f}M'
                )
else:
    st.warning('No metrics data available for the selected filters.')
