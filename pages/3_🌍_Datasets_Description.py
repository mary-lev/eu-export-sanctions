import streamlit as st
import pandas as pd

# Set the page configuration
st.set_page_config(
    page_title="Trade Data Analysis",
    page_icon="📊",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    st.markdown('''
    ### About
    This project hypothesizes that Russia is circumventing EU sanctions 
    by increasing trade through intermediary countries such as Kyrgyzstan and Armenia, 
    which is reflected in anomalous trade data patterns post-2022.
    ''')
    st.write("Use the tabs above to explore different sections.")

# Main Content
st.title("📊 Trade Data Analysis")

# Tabs for structuring information
tab1, tab3, tab4, tab5 = st.tabs([
    "Datasets Overview",
    "Legal & Ethical Analysis",
    "Technical Details",
    "Sustainability",
])

# ------------------- Datasets Overview -------------------
with tab1:
    st.write("### Datasets Overview")
    # Dataset information
    datasets = [
        {
            "Name": "Eurostat Trade Data",
            "Source": '<a href="https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database" target="_blank">Eurostat</a>',
            "Description": "Official harmonized data on exports and imports between EU member states and with non-EU countries.",
            "Time Period": "2019 - 2024",
            "Variables": "Reporting country, Partner country, Product categories (HS codes), Trade flow (export/import), Value in EUR, Period (monthly)",
            "Format": "CSV files",
            "License": '<a href="https://ec.europa.eu/info/legal-notice_en#reuse" target="_blank">European Commission Reuse Policy</a>'
        },
        {
            "Name": "Kyrgyzstan State Trade Statistics",
            "Source": '<a href="https://stat.gov.kg/ru/statistics/vneshneekonomicheskaya-deyatelnost/" target="_blank">National Statistical Committee of the Kyrgyz Republic</a>',
            "Description": "Data on geographic distribution of Kyrgyzstan's imports of goods.",
            "Time Period": "2008 - 2023",
            "Variables": "Trade values in thousand USD, Partner countries (including EU, CIS, SCO, EAEU), Yearly data",
            "Format": "XLSX (Excel)",
            "License": '<a href="http://www.opendefinition.org/licenses/cc-by" target="_blank">Creative Commons Attribution</a>'
        },
        {
            "Name": "Armenian State Trade Statistics",
            "Source": '<a href="https://data.opendata.am/dataset/armenia-external-trade-database-2017-2023" target="_blank">Open Data Armenia</a>',
            "Description": "Data on Armenia's external trade activities (imports and exports).",
            "Time Period": "2017 - 2023",
            "Variables": "Trade values in thousand USD, Trade partners (countries), Monthly data",
            "Format": "CSV",
            "License": '<a href="https://opendatacommons.org/licenses" target="_blank">Other (Public Domain)</a>'
        },
        {
            "Name": "Uzbekistan State Trade Statistics",
            "Source": '<a href="https://stat.uz/en/official-statistics/merchandise-trade" target="_blank">National Statistical Committee of the Republic of Uzbekistan</a>',
            "Description": "Data on Uzbekistan's trade activities with various partners.",
            "Time Period": "2010 - 2023",
            "Variables": "Trade values in thousand USD, Trade partners (countries), Yearly data",
            "Format": "CSV",
            "License": "Not specified"
        },
        {
            "Name": "Kazakhstan State Trade Statistics",
            "Source": '<a href="https://stat.gov.kz/en/industries/economy/foreign-market/spreadsheets/?year=2021&name=47218&period=&type=" target="_blank">Bureau of National Statistics</a>',
            "Description": "Data on Kazakhstan's trade activities with various partners (imports and exports).",
            "Time Period": "2021 - 2024",
            "Variables": "Trade values in thousand USD, Trade partners (countries), Yearly data",
            "Format": "XLSX",
            "License": "Not specified"
        },
        {
            "Name": "Russian Trade Data",
            "Source": '<a href="https://customs.gov.ru/statistic/vneshn-torg/vneshn-torg-countries" target="_blank">Federal Custom Service of Russia</a>, <a href="https://eng.rosstat.gov.ru/" target="_blank">Rosstat</a>',
            "Description": "Partial data on Russia's trade activities with various partners.",
            "Time Period": "2011 - 2022",
            "Variables": "Trade values, Trade partners by regions, Yearly data",
            "Format": "XLSX, XLS",
            "License": "Not specified"
        }
    ]

    df = pd.DataFrame(datasets)

    # Display HTML-enabled table
    st.markdown(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

    st.subheader("Eurostat Data Sample")
    eurostat_sample = pd.DataFrame({
        'REPORTER': ['Germany', 'France'],
        'PARTNER': ['Kyrgyzstan', 'Armenia'],
        'PRODUCT': ['Total', 'Total'],
        'FLOW': ['EXPORT', 'EXPORT'],
        'PERIOD': ['Aug. 2023', 'Aug. 2023'],
        'VALUE_IN_EUR': [5000000, 3000000]
    })
    st.dataframe(eurostat_sample)

    st.subheader("Datasets Provenance and Typology")
    st.write('''
    - **Provenance**:
        - **Eurostat Data**: Sourced from the official European Union statistical office, providing reliable and standardized trade data.
        - **State Agency Data**: Datasets from Armenia, Russia, Kyrgyzstan, Kazakhstan, and Uzbekistan are sourced from their respective national statistical agencies. However, these agencies often do not provide detailed metadata or clear licensing information, which poses challenges for data integration and reuse.
    - **Typology**:
        - The datasets include both **quantitative data** (trade values) and **categorical data** (countries, trade direction).
        - **Variations in Variables**: While Eurostat data includes detailed variables like product categories (HS codes) and monthly periods, the state agency data often provides aggregated yearly data without detailed breakdowns.
    - **Format**:
        - **Eurostat**: Data is provided in CSV format, which is widely accepted and easy to process.
        - **State Agencies**: Data is provided in various formats such as XLSX (Excel) and CSV, sometimes with inconsistent structures.
    - **Metadata and License**:
        - **Eurostat**: Provides comprehensive metadata specifying variables, units, and licensing terms under the [European Commission Reuse Policy](https://ec.europa.eu/info/legal-notice_en#reuse).
        - **State Agencies**:
            - **Lack of Metadata**: Armenia, Russia, Kyrgyzstan, and Kazakhstan do not provide detailed metadata with their datasets.
            - **Licensing Uncertainties**: Not all datasets from these agencies specify licensing terms, which raises concerns about legal reuse. For example, Uzbekistan and Kazakhstan do not have clear license information.
        - **Implications**:
            - The absence of metadata requires additional effort to understand and process the data correctly.
            - Unspecified licenses necessitate cautious use of the data, adhering to fair use principles and ensuring proper attribution where possible.
''')

    st.subheader("Quality and Accuracy Assessment")
    st.write('''
    - **Completeness**:
        - **Time Period Variations**:
            - Datasets cover varying time periods, making it challenging to align them perfectly for analysis.
            - For instance, Eurostat data spans **2010 - 2024**, while Armenia's data is available from **2017 - 2023**, and Kazakhstan's data covers **2021 - 2024**.
        - **Data Gaps**. Some datasets lack monthly granularity, limiting the depth of temporal analysis.
    - **Accuracy**:
        - **Currency and Units Discrepancies**. Eurostat reports trade values in **euros (EUR)**, while state agencies report in **thousand US dollars (USD)**. This requires careful currency conversion and unit adjustments to ensure accurate comparisons.
        - **Inconsistent Country Names**. In the Eurostat dataset for certain years (e.g., 2016), country names are listed in different languages or spellings (e.g., 'Ouzbekistan' for Uzbekistan, 'Kirghizistan' for Kyrgyzstan, 'Arménie' for Armenia). These inconsistencies caused issues during data processing, necessitating the standardization of country names to maintain consistency across datasets.
        - **Data Reliability**. While Eurostat data is assumed to be highly reliable due to standardized collection methods, the accuracy of state agency data may vary due to differences in data collection practices and potential political influences.
    - **Consistency**:
        - **Standardization Efforts**:
            - Variable names and data formats have been standardized across datasets to facilitate integration.
            - Date formats have been unified, and numeric values have been converted to consistent units and currencies.
        - **Challenges**:
            - Lack of metadata from state agencies required manual inspection to understand variable meanings and units.
            - Inconsistent data structures and file formats added complexity to the data cleaning process.
    ''')


    st.subheader("Privacy Compliance")
    st.write('''
    - **Personal Data**. All datasets are aggregated at the country level and do not include any personal or sensitive individual data.
    - **Anonymization** not required, as the data does not contain personally identifiable information (PII).
    - **Note**: Despite the absence of personal data, careful handling is necessary to respect any proprietary information and comply with data usage terms, especially given the lack of explicit licensing from some state agencies.
    ''')


# ------------------- Legal & Ethical Analysis -------------------
with tab3:
    st.header("Legal & Ethical Analysis")
    st.subheader("Legal Considerations")
    st.write('''
    **Licensing and Data Availability:**
    - **Eurostat Data**:
        - License: [European Commission Reuse Policy](https://ec.europa.eu/info/legal-notice_en#reuse)
        - Terms: Free reuse with mandatory source acknowledgment.
        - Compliance: Properly cited Eurostat as the data source.
    - **State Agency Data**:
        - **Russia**:
            - **Limited Data Availability**: After the onset of the war in 2022, Russia significantly restricted access to detailed trade data.
            - **Data Provided**: Only aggregated trade figures by broad regions (e.g., Europe, Asia) are available, without detailed country-level data.
            - **License and Usage Terms**: The data comes with specific usage conditions, including mandatory attribution.
                - *When using information in mass media, please provide a reference: "According to data from the Federal Customs Service of Russia, posted on the official website of the FCS of Russia".*
            - **Compliance**: Ensured adherence to the usage terms by providing appropriate attribution when referencing Russian data.
        - **Other State Agencies**:
            - Licensing information is often unclear or not specified.
            - Used data cautiously, adhering to fair use principles and providing attribution where possible.

    **Data Limitations and Legal Implications:**
    - The lack of detailed Russian trade data post-2022 poses challenges for comprehensive analysis.
    - Reliance on aggregated data limits the ability to identify specific trade patterns or anomalies at the country level.
    - **Legal Considerations**:
        - Must respect any restrictions on data use imposed by the data providers.
        - Avoid unauthorized use or distribution of restricted data.
    ''')

    st.subheader("Ethical Considerations")
    st.write('''
    **Data Gaps and Biases:**
    - **Impact of Limited Russian Data**:
        - The absence of detailed Russian trade data could introduce biases in the analysis.
        - There's a risk of overemphasizing anomalies in intermediary countries without fully understanding Russia's direct trade activities.
    - **Mitigation Strategies**:
        - Acknowledge the data limitations openly in the analysis.
        - Use alternative data sources where possible, such as mirror statistics from Russia's trade partners.

    **Transparency and Responsibility:**
    - **Transparency**:
        - Clearly communicate the limitations of the data and the potential impact on the findings.
        - Provide context about the geopolitical situation affecting data availability.
    - **Responsibility**:
        - Avoid drawing definitive conclusions solely based on incomplete data.
        - Present findings cautiously, emphasizing that they are based on the best available information.

    **Ethical Use of Data:**
    - **Attribution and Compliance**:
        - Adhere to the usage conditions specified by data providers, including attribution requirements.
    - **Respect for Data Restrictions**:
        - Avoid attempting to access or use restricted data through unethical means.
        - Respect any embargoes or limitations imposed by data sources.

    **Implications for Analysis:**
    - The limited availability of Russian data highlights the importance of ethical considerations in handling sensitive geopolitical information.
    - The analysis must balance the need for insightful findings with respect for legal and ethical boundaries.
    ''')

# ------------------- Technical Details -------------------
with tab4:
    st.header("Technical Analysis")
    st.write('''
    In this section, we provide a detailed technical analysis of the initial datasets used in the project. This includes an examination of data formats, structures, consistency, metadata availability, data integration challenges, and preprocessing steps required for effective use.
    ''')

    st.subheader("1. Eurostat Trade Data")

    st.write('''
    **Format and Structure:**

    - **Format:** CSV files.
    - **Encoding:** UTF-8.
    - **Structure:** Well-structured with consistent columns across files, including variables such as `REPORTER`, `PARTNER`, `PRODUCT`, `FLOW`, `PERIOD`, and `VALUE_IN_EUR`.

    **Data Characteristics:**

    - **Temporal Coverage:** 2010 - 2024.
    - **Granularity:** Monthly data, allowing for detailed temporal analysis.
    - **Variables:**
        - `REPORTER`: EU member state reporting the trade data.
        - `PARTNER`: Partner country involved in the trade.
        - `PRODUCT`: Commodity classification, usually using HS codes.
        - `FLOW`: Direction of trade (`EXPORT` or `IMPORT`).
        - `PERIOD`: Month and year of the trade data.
        - `VALUE_IN_EUR`: Trade value in euros.

    **Metadata and Documentation:**

    - **Availability:** Comprehensive metadata provided, including variable definitions and data collection methodologies.
    - **License Information:** Clearly specified under the European Commission's reuse policy.

    **Technical Considerations:**

    - **Data Consistency:** High consistency due to standardized reporting.
    - **Challenges:**
        - **Language Variations:** Some country names appear in different languages (e.g., 'Arménie' for Armenia), requiring standardization.
        - **Large File Sizes:** May require efficient data handling techniques.

    **Preprocessing Steps:**

    - Standardize country names using ISO country codes.
    - Parse `PERIOD` strings into datetime objects.
    - Filter data for relevant flows and partner countries.
    ''')

    # Repeat similar structure for other datasets
    st.subheader("2. Kyrgyzstan State Trade Statistics")
    st.write('''
    **Format and Structure:**

    - **Format:** XLSX (Excel) files.
    - **Structure:** Custom formats with merged cells and non-standard layouts.

    **Data Characteristics:**

    - **Temporal Coverage:** 2008 - 2023.
    - **Granularity:** Yearly data.
    - **Variables:**
        - Trade values in thousand USD.
        - Partner countries, sometimes grouped by regions.

    **Metadata and Documentation:**

    - **Availability:** Limited metadata.
    - **License Information:** Listed as Creative Commons Attribution, but detailed terms may not be explicitly provided.

    **Technical Considerations:**

    - **Challenges:**
        - **Non-Standard Formats:** Requires manual inspection to identify data tables.
        - **Currency and Units:** Values are in thousand USD, needing conversion.

    **Preprocessing Steps:**

    - Parse Excel files using libraries like `pandas`.
    - Normalize headers.
    - Convert currencies and adjust units.
    ''')

    # Continue for the remaining datasets (Armenian, Uzbek, Kazakh, Russian data)
    # Due to space constraints, I'll summarize the remaining datasets

    st.subheader("3. Armenian State Trade Statistics")
    st.write('''
    **Format and Structure:** CSV files with variables like `country`, `year`, `import_consigment`.

    **Challenges:**

    - Missing values represented as '-', requiring cleaning.
    - Currency conversion from thousand USD to EUR.

    **Preprocessing Steps:**

    - Replace placeholders with `NaN`.
    - Convert data types and currencies.
    - Standardize date formats.
    ''')

    st.subheader("4. Uzbekistan State Trade Statistics")
    st.write('''
    **Format and Structure:** CSV files, may require reshaping from wide to long format.

    **Challenges:**

    - Lack of metadata necessitates inference of variable meanings.
    - Currency conversion needed.

    **Preprocessing Steps:**

    - Reshape data using `melt` functions.
    - Convert units and currencies.
    - Standardize country names.
    ''')

    st.subheader("5. Kazakhstan State Trade Statistics")
    st.write('''
    **Format and Structure:** XLSX files with non-standard formats.

    **Challenges:**

    - Data extraction from non-standard Excel files.
    - Possible language barriers with Russian or Kazakh headers.

    **Preprocessing Steps:**

    - Use `pandas` to parse Excel files.
    - Translate headers if necessary.
    - Convert trade values to consistent units and currencies.
    ''')

    st.subheader("6. Russian Trade Data")
    st.write('''
    **Format and Structure:** XLSX/XLS files with aggregated data by regions.

    **Challenges:**

    - Limited granularity limits detailed analysis.
    - Access restrictions and language barriers.

    **Preprocessing Steps:**

    - Translate data from Russian to English.
    - Extract relevant aggregated data.
    - Ensure compliance with attribution requirements.
    ''')

    st.subheader("Integration Challenges and Solutions")
    st.write('''
    **Data Harmonization:**

    - Standardize country names using ISO codes.
    - Align date formats to ISO 8601.
    - Convert all trade values to EUR and adjust units.

    **Handling Missing Metadata:**

    - Infer variable meanings based on context.
    - Create internal documentation for assumptions.

    **Data Quality Assurance:**

    - Cross-validate with alternative sources where possible.
    - Implement checks for inconsistent data.

    **Data Transformation:**

    - Reshape data to consistent formats suitable for analysis.
    - Merge datasets on common keys with careful handling of temporal granularity differences.

    **Language Barriers:**

    - Use translation tools for non-English data.
    - Ensure consistent encoding with UTF-8.

    **Legal and Ethical Compliance:**

    - Be cautious with datasets lacking clear licenses.
    - Include required attributions, especially for Russian data.
    ''')

    st.write('''
    **Note:** For a more detailed technical analysis, additional information on data samples, preprocessing steps, exchange rates used, and data limitations would be helpful.
    ''')

# ------------------- Sustainability -------------------
with tab5:
    st.header("Sustainability & Lifecycle")
    st.write('''
    Ensuring the sustainability of datasets is crucial for the long-term viability and relevance of the project. However, several challenges affect the sustainability of the datasets used in this analysis.

    **Challenges:**

    - **Manual Data Collection.** The datasets are currently downloaded manually in CSV or XLSX formats from state websites. This process is time-consuming and prone to human error. Manual updates are not scalable for regular data refreshes.

    - **Accessibility of Russian Data.** Russian state data is only accessible through a Russian VPN, making it difficult to obtain from Europe due to regional restrictions and potential legal considerations. Reliance on such restricted access poses significant sustainability risks, as data availability can change without notice.

    **Implications for Sustainability:**

    - **Data Currency and Updates.** The inability to automate data retrieval means that datasets may become outdated if not manually refreshed regularly. Delays in updating data can affect the accuracy and relevance of the analysis.

    - **Data Reliability and Continuity.** Dependence on manual downloads from state websites may be impacted by website changes, data removal, or access restrictions. There is a risk of data sources becoming unavailable, which would hinder ongoing analysis.

    **Limitations Acknowledgment.** Recognize that despite mitigation efforts, some sustainability challenges may persist due to factors beyond control, such as geopolitical events or changes in data publication policies. Acknowledge these limitations in the analysis and consider them when interpreting results.

    **Conclusion.**  While there are significant challenges to the sustainability of the datasets due to manual collection methods and accessibility issues, particularly with Russian data, proactive strategies can help mitigate some of these concerns. By exploring alternative data sources, automating data retrieval where possible, and maintaining thorough documentation, the project can enhance the sustainability and reliability of its datasets.
    Ongoing evaluation of data sources and adaptability in data collection approaches will be essential to maintain the project's relevance and impact over time.
    ''')

st.write("---")
st.write("For more information, navigate through the sidebar or contact the project team.")
