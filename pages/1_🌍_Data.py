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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Datasets Overview",
    "Data Integration & Quality",
    "Legal & Ethical Analysis",
    "Technical Details",
    "Sustainability",
    "Analysis Highlights"
])

# ------------------- Datasets Overview -------------------
with tab1:
    st.header("Datasets Overview")
    st.write('''
    This section provides an overview of the datasets used in the project.
    Each dataset is assessed for its source, description, variables, and availability.
    ''')
    
    datasets = [
        {
            "Name": "Eurostat Trade Data",
            "Source": "[Eurostat](https://ec.europa.eu/eurostat/web/international-trade-in-goods/data/database)",
            "Description": "Official harmonized data on exports and imports between EU member states and with non-EU countries.",
            "Time Period": "2019 - 2024",
            "Variables": ["Reporting country", "Partner country", "Product categories (HS codes)", "Trade flow (export/import)", "Value in EUR", "Period (monthly)"],
            "Format": "CSV files",
            "License": "[European Commission Reuse Policy](https://ec.europa.eu/info/legal-notice_en#reuse)"
        },
        # Add the other datasets similarly...
    ]

    for dataset in datasets:
        st.subheader(dataset["Name"])
        st.write(f"- **Source**: {dataset['Source']}")
        st.write(f"- **Description**: {dataset['Description']}")
        st.write(f"- **Time Period**: {dataset['Time Period']}")
        st.write("- **Variables**:")
        st.write(", ".join(dataset["Variables"]))
        st.write(f"- **Format**: {dataset['Format']}")
        st.write(f"- **License**: {dataset['License']}")

    # Example Data Previews
    if st.checkbox("Show Example Data Previews"):
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

# ------------------- Data Integration & Quality -------------------
with tab2:
    st.header("Data Integration & Quality")
    st.write('''
    This section discusses how datasets were integrated and evaluated for quality.
    ''')
    
    st.subheader("Data Integration Methodology")
    st.write('''
    - **Time Period Standardization**: Aligned datasets to the period 2019–2024.
    - **Currency Conversion**: Converted data from USD to EUR using historical exchange rates.
    - **Data Cleaning**: Handled missing values, corrected data types, and removed duplicates.
    - **Data Transformation**: Normalized structures for consistency.
    - **Validation**: Cross-checked aggregated values with official reports.
    ''')

    st.subheader("Data Quality Assessment")
    st.write('''
    - **Completeness**: Coverage varies by dataset; Eurostat data is most comprehensive.
    - **Consistency**: Variable names and formats were standardized.
    - **Accuracy**: Data is assumed reliable but cross-validated where possible.
    ''')

# ------------------- Legal & Ethical Analysis -------------------
with tab3:
    st.header("Legal & Ethical Analysis")
    st.subheader("Legal Considerations")
    st.write('''
    - **Licensing Compliance**: Proper attribution and adherence to license terms for all datasets.
    - **Privacy**: No personal data; all data is aggregated.
    - **Usage Purpose**: Strictly for educational and research purposes.
    ''')

    st.subheader("Ethical Considerations")
    st.write('''
    - Avoided biases in data representation.
    - Ensured transparency in methodologies.
    - Acknowledged limitations and assumptions openly.
    ''')

# ------------------- Technical Details -------------------
with tab4:
    st.header("Technical Details")
    st.subheader("Data Formats and Metadata")
    st.write('''
    - Standardized formats: CSV with UTF-8 encoding.
    - Metadata: Followed DCAT-AP standards.
    - Provenance: Documented sources, processing steps, and transformations.
    ''')

# ------------------- Sustainability -------------------
with tab5:
    st.header("Sustainability")
    st.subheader("Data Refresh Strategy")
    st.write('''
    - Automated data retrieval scripts for regular updates.
    - Scheduled updates and version control using Git.
    ''')

    st.subheader("Long-Term Goals")
    st.write('''
    - Expand datasets to include more countries and variables.
    - Build a community for ongoing contributions and usage.
    ''')

# ------------------- Analysis Highlights -------------------
with tab6:
    st.header("Analysis Highlights")
    st.write('''
    Key findings and insights from the project will be highlighted here.
    ''')

    st.subheader("Trade Anomalies")
    st.write('''
    - Significant increases in trade flows through intermediary countries post-2022.
    - Patterns suggest potential sanctions circumvention.
    ''')

    st.subheader("Limitations")
    st.write('''
    - Limited data availability for certain regions.
    - Reporting discrepancies and currency fluctuations affect analysis.
    ''')

# Footer
st.write("---")
st.write("For more information, navigate through the sidebar or contact the project team.")
