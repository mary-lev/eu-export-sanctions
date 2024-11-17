import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page config
st.set_page_config(
    page_title='Data Sources & Methodology',
    page_icon='📊',
    layout='wide'
)

# Add sidebar
with st.sidebar:
    st.title('Navigation')
    st.write('You are currently on: Data Sources & Methodology')
    
    # Add any page-specific filters
    st.subheader('Data Source Filters')
    data_sources = st.multiselect(
        'Select Data Sources',
        ['Eurostat', 'Kyrgyzstan Statistics', 'Russian Trade Data'],
        default=['Eurostat']
    )

# Main content
st.title('📊 Data Sources & Methodology')

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(['Data Sources', 'Methodology', 'Limitations'])

with tab1:
    st.header('Data Sources')
    st.write('''
    This analysis uses data from multiple sources to create a comprehensive picture
    of trade patterns:
    
    1. **Eurostat**
       - International trade in goods (ITG) statistics measure the value and quantity of goods traded between the EU countries (intra-EU trade) and goods traded by EU countries with non-EU countries (extra-EU trade). The term ‘goods’ refers to all movable property.
       - These are the official, harmonised source of information about exports, imports, and trade balances of the EU, its members, and the euro area.
       - The statistics are compiled based on concepts and definitions set out in EU legislation to ensure consistency and reliability.
       - **Time period covered**: 2019 - 2024
       - **Variables included**: Export value, Import value, Country of origin/destination, Product categories.

    2. **Kyrgyzstan Statistics**
       - The [import](https://data.gov.kg/dataset/nmnopt-tobapob) and [export](https://data.gov.kg/dataset/ekcnopt-tobapob/resource/d66a2b70-ceb6-4793-bd17-b20f805f9275) datasets provide detailed insights into Kyrgyzstan's trade activities.
       - **Time period covered**: 2016 - 2023
       - **Variables included**:
         - Sectoral breakdown of imports and exports (e.g., agriculture, mining, manufacturing, services).
         - Yearly trade values in thousand USD.
       - **Import Data**:
         - Last updated: 4 October 2024
         - Created: 4 October 2024
         - Format: XLSX (Microsoft Excel Spreadsheet)
         - Size: 16 KiB
         - License: Creative Commons Attribution
       - **Export Data**:
         - Last updated: 4 October 2024
         - Created: 2 March 2024
         - Format: XLSX (Microsoft Excel Spreadsheet)
         - Size: 13.9 KiB
         - License: Creative Commons Attribution
       
    3. **Russian Trade Data**
       - Limited data is available from Russian sources, given that much of the trade data has been restricted since the war began.
       - **Time period covered**: 2019 - 2022 (limited availability)
       - **Variables included**: Export/Import value, Trade partners, Product categories.
    ''')

    # Add example data preview
    if st.checkbox('Show Data Preview'):
        # Example dataset from Eurostat
        data = {
            'REPORTER': ["Luxembourg", "Cyprus", "Greece", "Portugal", "Romania"],
            'PARTNER': ["Russian Federation (Russia)"] * 5,
            'PRODUCT': ["Total"] * 5,
            'FLOW': ["EXPORT"] * 5,
            'STAT_PROCEDURE': ["Total"] * 5,
            'PERIOD': ["Aug. 2024"] * 5,
            'VALUE_IN_EUR': [162950, 179808, 6715293, 7379470, 11732919]
        }
        df = pd.DataFrame(data)
        st.dataframe(df.head())
