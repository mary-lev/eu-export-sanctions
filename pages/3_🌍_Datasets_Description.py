import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Trade Data Analysis",
    page_icon="📊",
    layout="wide"
)

with st.sidebar:
    st.title("Navigation")
    st.markdown('''
    ### About
    This project hypothesizes that Russia is circumventing EU sanctions 
    by increasing trade through intermediary countries such as Kyrgyzstan and Armenia, 
    which is reflected in anomalous trade data patterns post-2022.
    ''')
    st.write("Use the tabs above to explore different sections.")

st.title("📊 Trade Data Analysis")

tab1, tab3, tab4, tab5 = st.tabs([
    "Datasets Overview",
    "Legal & Ethical Analysis",
    "Technical Details",
    "Sustainability",
])

# ------------------- Datasets Overview -------------------
with tab1:
    st.write("### Datasets Overview")
    datasets = [
        {
            "Name": "Eurostat Trade Data",
            "Source": '<a href="https://ec.europa.eu/eurostat/cache/metadata/en/ext_go_detail_sims.htm" target="_blank">Eurostat</a>',
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
            "Format": "CSV, JSON-L, Parquet",
            "License": '<a href="https://opendatacommons.org/licenses" target="_blank">Other (Public Domain)</a>'
        },
        {
            "Name": "Uzbekistan State Trade Statistics",
            "Source": '<a href="https://stat.uz/en/official-statistics/merchandise-trade" target="_blank">National Statistical Committee of the Republic of Uzbekistan</a>',
            "Description": "Data on Uzbekistan's trade activities with various partners.",
            "Time Period": "2010 - 2023",
            "Variables": "Trade values in thousand USD, Trade partners (countries), Yearly and monthly data",
            "Format": "XLSX, PDF, CSV, JSON (API), XML (API)",
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

    st.markdown(
        df.to_html(escape=False, index=False),
        unsafe_allow_html=True
    )

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
        - **Time Period Variations**. Datasets cover varying time periods, making it challenging to align them perfectly for analysis. For instance, Eurostat data spans **2010 - 2024**, while Armenia's data is available from **2017 - 2023**, and Kazakhstan's data covers **2021 - 2024**.
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
    - **Mitigation Strategies**: Acknowledge the data limitations openly in the analysis.

    **Transparency and Responsibility:**
    - **Transparency**:
        - Clearly communicate the limitations of the data and the potential impact on the findings.
        - Provide context about the geopolitical situation affecting data availability.
    - **Responsibility**:
        - Avoid drawing definitive conclusions solely based on incomplete data.
        - Present findings cautiously, emphasizing that they are based on the best available information.

    **Implications for Analysis:**
    - The limited availability of Russian data highlights the importance of ethical considerations in handling sensitive geopolitical information.
    - The analysis must balance the need for insightful findings with respect for legal and ethical boundaries.
    ''')

# ------------------- Technical Details -------------------
with tab4:
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
    ''')
    import pandas as pd
    eurostat_sample = pd.DataFrame({
        'REPORTER': ['Germany', 'France'],
        'PARTNER': ['Kyrgyzstan', 'Armenia'],
        'PRODUCT': ['Total', 'Total'],
        'FLOW': ['EXPORT', 'EXPORT'],
        'PERIOD': ['Aug. 2023', 'Aug. 2023'],
        'VALUE_IN_EUR': [5000000, 3000000]
    })
    st.dataframe(eurostat_sample)

    st.subheader("2. Kyrgyzstan State Trade Statistics")
    st.write('''
    **Format and Structure:**

    - **Format:** Single XLSX (Excel) file ("4.03.00.20 Географическое распределение импорта товаров.xlsx").
    - **Structure:** Custom formats with merged cells and non-standard layouts.

    **Data Characteristics:**

    - **Temporal Coverage:** 1994 - 2023.
    - **Granularity:** Yearly data.
    - **Variables:**
        - Trade values in thousand USD.
        - Partner countries, additionally grouped by regions.

    **Metadata and Documentation:**

    - **Availability:** No metadata provided.
    - **License Information:** No explicit licensing terms.

    **Technical Considerations:**

    - **Challenges:**
        - Non-Standard Format requires manual inspection to identify data tables.
        - Missing values represented as '-', requiring cleaning.
        - Values are in thousand USD, needing conversion.
    ''')

    data = {
        "4.03.00.20: Geographic distribution of imports of goods": ["Total", "The EU", "CIS", "SCO", "EAEU", "Europe", "Austria", "Albania", "Andorra", "Belarus"],
        "1994": [317004.7, 20939.5, 209275.8, "-", "-", 98821.0, 513.3, "-", "-", 2576.6],
        "1995": [522334.9, 44721.2, 353284.4, "-", "-", 171661.6, 1324.8, "-", "-", 5034.0],
        "1996": [837688.2, 113532.3, 485310.2, "-", "-", 322572.3, 9817.9, "-", "-", 6104.0],
        "1997": [709304.9, 106643.2, 432688.8, "-", "-", 316654.9, 4065.5, "-", "-", 10260.6]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)

    st.subheader("3. Armenian State Trade Statistics")
    st.write('''
    **Format and Structure:** Single CSV file with variables like `country`, `year`, `import_consigment`.
    No metadata provided.

    **Challenges:**

    - Missing values represented as '-', requiring cleaning.
    - Lack of metadata necessitates inference of variable meanings.
    - Currency conversion from thousand USD to EUR.
    ''')
    data = {
        "country": ["Afghanistan"] * 8,
        "export": ["-", 573.4, 210.6, 196.6, 1081.8, 123.1, 807.2, 3326.0],
        "import_consignment": ["-", "-", "-", "-", "-", "-", "-", 0.2],
        "import_origin": [0.1, "-", "-", "-", "-", "-", "-", 0.3],
        "timeperiod": [5, 7, 8, 9, 10, 11, 12, "Year"],
        "year": [2020] * 8
    }

    df_afghanistan = pd.DataFrame(data)
    st.dataframe(df_afghanistan)

    st.subheader("4. Uzbekistan State Trade Statistics")
    st.write('''
    **Format and Structure:** Single CSV file, using "Commodity nomenclature foreign economic activities Republic of Uzbekistan".

    **Challenges:** Limited metadata & currency conversion needed.
    ''')
    uz_data = {
        "Code": [192, 384, 598, 798],
        "Klassifikator": ["Kuba", "Kot D'ivuar", "Papua - Yangi Gvineya", "Tuvalu"],
        "Klassifikator_ru": ["Куба", "Кот-д'Ивуар", "Папуа-Новая Гвинея", "Тувалу"],
        "Klassifikator_en": ["Cuba", "Côte d’Ivoire", "Papua New Guinea", "Tuvalu"],
        "2010": [0.03, 10.0, 0.0, 0.0],
        "2011": [1.67, 40.0, 0.0, 0.0],
        "2012": [0.0, 50.5, 0.0, 0.0],
        "2013": [0.0, 150.0, 0.0, 0.0],
        "2014": [0.0, 106.0, 0.0, 0.0],
        "2015": [0.0, 31.5, 0.0, 0.0],
        "2016": [0.69, 21.72, 0.0, 0.0],
        "2017": [0.67, 29.87, 0.04, 0.0],
        "2018": [6.19, 33.63, 0.0, 0.0],
        "2019": [11791.59, 85.29, 0.0, 0.0],
        "2020": [17.13, 69.76, 0.0, 0.0],
        "2021": [18.2, 641.96, 0.0, 0.0],
        "2022": [59.1, 1772.81, 0.0, 0.0],
        "2023": [123.5, 1669.4, 43.0, 0.5]
    }
    df_trade = pd.DataFrame(uz_data)
    st.dataframe(df_trade)

    st.subheader("5. Kazakhstan State Trade Statistics")
    st.write('''
    **Format and Structure:** Yearly XLSX files in Russian with non-standard formats.
    No metadata or licensing information provided.

    **Challenges:**

    - Data extraction from non-standard Excel files.
    - Possible language barriers with Russian or Kazakh headers.
    ''')
    kz_data = {
        "Наименование области": ["Всего", "Страны СНГ", "Страны ЕАЭС", "Армения", "Беларусь", "Кыргызстан"],
        "Товарооборот": [101736459.9, 33237916.5, 26586658.8, 20817.4, 891029.2, 1050532.2],
        "Товарооборот (%)": [100.0, 32.7, 26.1, 0.0, 0.9, 1.0],
        "Экспорт": [60321024.4, 12493485.9, 7814129.5, 10332.8, 110295.8, 674755.2],
        "Экспорт (%)": [100.0, 20.7, 13.0, 0.0, 0.2, 1.1],
        "Импорт": [41415435.5, 20744430.6, 18772529.3, 10484.6, 780733.5, 375777.0],
        "Импорт (%)": [100.0, 50.1, 45.3, 0.0, 1.9, 0.9]
    }
    df_kz = pd.DataFrame(kz_data)
    st.dataframe(df_kz)

    st.subheader("6. Russian Trade Data")
    st.write('''
    **Format and Structure:** XLSX/XLS files with aggregated data by regions.

    **Challenges:** Limited granularity, access restrictions and language barriers.
    ''')
    ru_data = {
        "Группа стран": ["Весь мир", "ЕВРОПА", "АЗИЯ", "АФРИКА", "АМЕРИКА", "ОКЕАНИЯ"],
        "Экспорт 2022 (млрд. долл. США)": [592.5, 265.6, 290.4, 14.8, 20.5, 0.3],
        "Экспорт 2023 (млрд. долл. США)": [425.1, 84.9, 306.6, 21.2, 12.2, 0.0],
        "Темп роста экспорта (%)": [71.7, 32.0, 105.6, 142.9, 59.6, 2.5],
        "Импорт 2022 (млрд. долл. США)": [255.3, 89.5, 145.2, 3.1, 16.8, 0.4],
        "Импорт 2023 (млрд. долл. США)": [285.1, 78.5, 187.5, 3.4, 15.0, 0.2],
        "Темп роста импорта (%)": [111.7, 87.7, 129.2, 108.6, 89.0, 41.8]
    }
    df_ru = pd.DataFrame(ru_data)
    st.dataframe(df_ru)


# ------------------- Sustainability -------------------
with tab5:
    st.header("Sustainability & Lifecycle")
    st.write('''
    Ensuring the sustainability of datasets is crucial for the long-term viability and relevance of the project. However, several challenges affect the sustainability of the datasets used in this analysis.

    **Challenges:**

    - **Manual Data Collection.** The datasets are currently downloaded manually in CSV or XLSX formats from state websites. This process is time-consuming and prone to human error. Manual updates are not scalable for regular data refreshes.

    - **Accessibility of Russian Data.** Russian state data is only accessible through a Russian VPN, making it difficult to obtain from Europe due to regional restrictions and potential legal considerations. Reliance on such restricted access poses significant sustainability risks, as data availability can change or disappear without notice.

    **Implications for Sustainability.** Dependence on manual downloads from state websites may be impacted by website changes, data removal, or access restrictions. There is a risk of data sources becoming unavailable, which would hinder ongoing analysis.

    **Limitations Acknowledgment.** Recognize that despite mitigation efforts, some sustainability challenges may persist due to factors beyond control, such as geopolitical events or changes in data publication policies. Acknowledge these limitations in the analysis and consider them when interpreting results.
    ''')

st.write("---")