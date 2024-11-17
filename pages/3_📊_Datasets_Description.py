# pages/3_Datasets.py

import streamlit as st
import pandas as pd

# Set the page config
st.set_page_config(
    page_title='Datasets Description',
    page_icon='📂',
    layout='wide'
)

with st.sidebar:
    st.markdown('''
    ### About
    This project hypothesizes 
    that Russia is circumventing EU sanctions 
    by increasing trade through intermediary countries 
    such as Kyrgyzstan and Armenia, 
    which is reflected in anomalous trade data patterns post-2022.
    ''')

# Main content
st.title('📂 Datasets Description')

# Create tabs for organization
tab1, tab2, tab3 = st.tabs(['Datasets Overview', 'Data Integration', 'Data Quality'])

with tab1:
    st.header('Datasets Overview')
    st.write('''
    ## 1. Eurostat Trade Data

    - **Source**: [Eurostat](https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database)
    - **Description**: Official harmonized data on exports and imports between EU member states and with non-EU countries.
    - **Time Period**: 2019 - 2024
    - **Variables**:
        - Reporting country
        - Partner country
        - Product categories (HS codes)
        - Trade flow (export/import)
        - Value in EUR
        - Period (monthly)
    - **Format**: CSV files
    - **License**: [European Commission Reuse Policy](https://ec.europa.eu/info/legal-notice_en#reuse)

    ## 2. Kyrgyzstan Trade Statistics

    - **Source**: [National Statistical Committee of the Kyrgyz Republic](https://stat.kg/en/statistics/foreign-trade/)
    - **Description**: Data on Kyrgyzstan's imports and exports, including trade partners and sectoral breakdowns.
    - **Time Period**: 2016 - 2023
    - **Variables**:
        - Trade values in thousand USD
        - Partner countries
        - Sectoral categories
        - Yearly data
    - **Format**: XLSX (Excel)
    - **License**: [Creative Commons Attribution](https://creativecommons.org/licenses/by/4.0/)

    ## 3. Russian Trade Data

    - **Source**: Limited availability due to data restrictions.
    - **Description**: Partial data on Russia's trade activities with various partners.
    - **Time Period**: 2019 - 2022
    - **Variables**:
        - Trade values
        - Trade partners
        - Product categories
    - **Format**: Varies (CSV, XLSX)
    - **License**: Not specified
    ''')

    # Optionally display data previews
    if st.checkbox('Show Example Data Previews'):
        st.subheader('Eurostat Data Sample')
        # Load a sample dataset or use dummy data
        eurostat_sample = pd.DataFrame({
            'REPORTER': ['Germany', 'France'],
            'PARTNER': ['Kyrgyzstan', 'Armenia'],
            'PRODUCT': ['Total', 'Total'],
            'FLOW': ['EXPORT', 'EXPORT'],
            'PERIOD': ['Aug. 2023', 'Aug. 2023'],
            'VALUE_IN_EUR': [5000000, 3000000]
        })
        st.dataframe(eurostat_sample)

        st.subheader('Kyrgyzstan Import Data Sample')
        kyrgyz_import_sample = pd.DataFrame({
            'Year': [2021, 2022],
            'Trade Partner': ['EU', 'EU'],
            'Value (Thousand USD)': [200000, 400000]
        })
        st.dataframe(kyrgyz_import_sample)

with tab2:
    st.header('Data Integration Methodology')
    st.write('''
    ## Data Alignment

    - **Time Period Standardization**: All datasets are aligned to cover the period from 2019 to 2024.
    - **Currency Conversion**: Kyrgyzstan's data in USD is converted to EUR using historical exchange rates for accurate comparisons.
    - **Product Categorization**: Harmonized System (HS) codes are used to align product categories across datasets.

    ## Data Processing Steps

    1. **Data Loading**: Import datasets using pandas.
    2. **Data Cleaning**: Handle missing values, correct data types, and remove duplicates.
    3. **Data Transformation**: Normalize data structures for consistency.
    4. **Merging Datasets**: Combine data on common keys such as country and period.
    5. **Validation**: Cross-check aggregated values with official reports.

    ## Handling Missing Data

    - **Imputation**: For minor gaps, use interpolation methods.
    - **Exclusion**: In cases of significant missing data, exclude affected records with appropriate documentation.

    ## Tools and Technologies

    - **Programming Language**: Python
    - **Libraries**: pandas, numpy, plotly, streamlit
    - **Version Control**: Git and GitHub for code and data management
    ''')

with tab3:
    st.header('Data Quality and Limitations')
    st.write('''
    ## Quality Assessment

    - **Completeness**: Eurostat data is comprehensive for EU countries; Kyrgyzstan data is less detailed.
    - **Consistency**: Efforts made to standardize variable names and data formats.
    - **Accuracy**: Data is assumed accurate as per official sources but may have reporting delays or errors.

    ## Limitations

    - **Data Availability**: Russian trade data is limited post-2022 due to restrictions.
    - **Reporting Differences**: Variations in how countries report trade data can introduce inconsistencies.
    - **Currency Fluctuations**: Exchange rate volatility may affect value comparisons.

    ## Assumptions

    - **Data Reliability**: Official statistics are considered reliable unless evidence suggests otherwise.
    - **Static Economic Conditions**: Economic factors other than sanctions are assumed constant unless indicated.

    ## Ethical Considerations

    - **Data Privacy**: No personal data is used; all data is aggregated at the country level.
    - **Bias Mitigation**: Analysis aims to be objective, acknowledging limitations and avoiding unfounded conclusions.
    ''')

# Optional: Provide links to download datasets or view metadata
st.write('---')
st.write('For more details or to access the datasets, please refer to the [Data Sources & Methodology](4_Methodology) page.')
