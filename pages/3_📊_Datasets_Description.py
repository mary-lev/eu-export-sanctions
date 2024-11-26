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

    ## 2. Kyrgyzstan State Trade Statistics

    - **Source**: [National Statistical Committee of the Kyrgyz Republic](https://stat.gov.kg/ru/statistics/vneshneekonomicheskaya-deyatelnost/)
    - **Description**: Data on geographic distribution of Kyrgyzstan's imports of goods.
    - **Time Period**: 2008 - 2023
    - **Variables**:
        - Trade values in thousand USD
        - Partner countries, including grouping by regions (The EU, CIS, SCO, EAEU)
        - Yearly data
    - **Format**: XLSX (Excel)
    - **License**: [Creative Commons Attribution](http://www.opendefinition.org/licenses/cc-by)
    - **Note**: Data for 2023 is marked as preliminary.
    
    ## 3. Armenian State Trade Statistics
    - **Source**: [Statistical Committee of the Republic of Armenia through Open Data Armenia](https://data.opendata.am/dataset/armenia-external-trade-database-2017-2023)
    - **Description**: Data on Armenia's external trade activities (imports and exports).
    - **Time Period**: 2017 - 2023
    - **Variables**:
        - Trade values in thousand USD
        - Trade partners (countries)
        - Monthly data
    - **Format**: CSV
    - **License**: [Other (Public Domain)](https://opendatacommons.org/licenses)
    - **Updated**: April 4, 2023

    ## 4. Uzbekistan State Trade Statistics
             
    - **Source**: [National Statistical Committee of the Republic of Uzbekistan](https://stat.uz/en/official-statistics/merchandise-trade)
    - **Description**: Data on Uzbekistan's trade activities with various partners.
    - **Time Period**: 2010 - 2023
    - **Variables**:
        - Trade values in thousand USD
        - Trade partners (countries)
        - Yearly data
    - **Format**: CSV
             
    ## 5. Kazakhstan State Trade Statistics
             
    - **Source**: [Bureau of National Statistics, Agency for Strategic Planning and Reforms of the Republic of Kazakhstan](https://stat.gov.kz/en/industries/economy/foreign-market/spreadsheets/?year=2021&name=47218&period=&type=)
    - **Description**: Data on Kazakhstan's trade activities with various partners (imports and exports).
    - **Time Period**: 2021 - 2024
    - **Variables**:
        - Trade values in thousand USD
        - Trade partners (countries)
        - Yearly data
    - **Format**: XLSX
    - **License**: Not specified

    ## 6. Russian Trade Data

    - **Source**: [Federal Custom Service of R](https://customs.gov.ru/statistic/vneshn-torg/vneshn-torg-countries), [Federal State Statistics Service of Russia (Rosstat)](https://eng.rosstat.gov.ru/)
    - **Description**: Partial data on Russia's trade activities with various partners.
    - **Time Period**: 2011 - 2022
    - **Variables**:
        - Trade values
        - Trade partners by regions
        - Yearly data
    - **Format**: Varies (XLSX)
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

    ## Data Processing Steps

    1. **Data Loading**: Import datasets using pandas.
    2. **Data Cleaning**: Handle missing values, correct data types, and remove duplicates.
    3. **Data Transformation**: Normalize data structures for consistency.
    4. **Merging Datasets**: Combine data on common keys such as country and period.
    5. **Validation**: Cross-check aggregated values with official reports.

    ## Handling Missing Data

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
