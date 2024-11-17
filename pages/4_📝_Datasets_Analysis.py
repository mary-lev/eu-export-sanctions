# pages/4_Datasets_Analysis.py

import streamlit as st

# Set the page config
st.set_page_config(
    page_title='Datasets Analysis',
    page_icon='📝',
    layout='wide'
)

# Sidebar
with st.sidebar:
    st.title('Navigation')
    st.write('You are currently on: Datasets Analysis')

# Main content
st.title('📝 Datasets Analysis')

# Create tabs for each analysis section
tab_quality, tab_legal, tab_ethics, tab_technical, tab_sustainability = st.tabs([
    'Quality Analysis',
    'Legal Analysis',
    'Ethics Analysis',
    'Technical Analysis',
    'Sustainability'
])

# ------------------- Quality Analysis Tab -------------------
with tab_quality:
    st.header('Quality Analysis of the Datasets')

    st.write('''
    In this section, we assess the quality of the datasets used in this project, focusing on aspects such as completeness, consistency, accuracy, and timeliness.
    ''')

    st.subheader('Completeness')
    st.write('''
    - **Eurostat Data**: Comprehensive coverage of EU trade data from 2019 to 2024.
    - **Kyrgyzstan Data**: Yearly trade data available from 2016 to 2023.
    - **Russian Data**: Limited availability post-2022 due to data restrictions.
    ''')

    st.subheader('Consistency')
    st.write('''
    - Data formats have been standardized across datasets.
    - Variable names have been harmonized for easier integration.
    - Discrepancies in reporting periods and units have been addressed.
    ''')

    st.subheader('Accuracy')
    st.write('''
    - Official sources are assumed to provide accurate data.
    - Cross-validation between datasets where possible.
    - Noted potential reporting biases or errors in certain datasets.
    ''')

    st.subheader('Timeliness')
    st.write('''
    - Eurostat data is updated monthly.
    - Kyrgyzstan data is updated annually.
    - Russian data may have delays due to restrictions.
    ''')

    st.subheader('Validation Steps')
    st.write('''
    - Checked for missing values and outliers.
    - Verified data types and formats.
    - Ensured alignment of time periods across datasets.
    ''')

# ------------------- Legal Analysis Tab -------------------
with tab_legal:
    st.header('Legal Analysis (Privacy, License, Purpose, etc.)')

    st.write('''
    This section addresses the legal considerations related to the use of the datasets, including licensing, privacy concerns, and compliance with data usage policies.
    ''')

    st.subheader('Licensing Compliance')
    st.write('''
    - **Eurostat Data**:
      - License: European Commission's reuse policy.
      - Terms: Free reuse with obligatory source acknowledgment.
      - Compliance: We have cited Eurostat as the source of the data.
    - **Kyrgyzstan Data**:
      - License: Creative Commons Attribution 4.0 International (CC BY 4.0).
      - Terms: Allows sharing and adaptation with proper attribution.
      - Compliance: We have attributed the data to the National Statistical Committee of the Kyrgyz Republic.
    - **Russian Data**:
      - License: Not specified due to limited availability.
      - Compliance: Used cautiously, ensuring no breach of usage rights.
    ''')

    st.subheader('Privacy Considerations')
    st.write('''
    - **Personal Data**: No personal or sensitive individual data is used; datasets contain aggregated trade statistics.
    - **Data Protection**: Compliant with GDPR as no personal data is processed.
    ''')

    st.subheader('Usage Rights and Purpose')
    st.write('''
    - Data is used for educational and research purposes.
    - Analysis aligns with the permitted use under the respective licenses.
    - Proper attribution and adherence to usage terms are maintained.
    ''')

# ------------------- Ethics Analysis Tab -------------------
with tab_ethics:
    st.header('Ethics Analysis')

    st.write('''
    In this section, we examine the ethical implications of our data usage and analysis, ensuring fairness, transparency, and objectivity.
    ''')

    st.subheader('Avoiding Cognitive Biases')
    st.write('''
    - Acknowledged assumptions and limitations in data interpretation.
    - Avoided inferring causation solely from correlation.
    - Presented data objectively without overstating conclusions.
    ''')

    st.subheader('Fair Representation')
    st.write('''
    - Ensured intermediary countries are not unfairly characterized.
    - Provided context for trade anomalies beyond sanction circumvention.
    - Recognized legitimate economic activities and growth factors.
    ''')

    st.subheader('Transparency and Reproducibility')
    st.write('''
    - Fully disclosed data sources and methodologies.
    - Provided code and datasets under open licenses for verification.
    - Encouraged peer review and feedback to refine analysis.
    ''')

    st.subheader('Social Implications')
    st.write('''
    - Considered the potential impact of findings on international relations.
    - Avoided contributing to stigmatization or unjust policies towards involved countries.
    - Emphasized the importance of accurate data in policymaking.
    ''')

# ------------------- Technical Analysis Tab -------------------
with tab_technical:
    st.header('Technical Analysis (Formats, Metadata, URI, Provenance)')

    st.write('''
    This section details the technical aspects of data handling, including formats, metadata standards, URI usage, and provenance documentation.
    ''')

    st.subheader('Data Formats')
    st.write('''
    - All datasets have been converted to standardized formats (CSV, UTF-8 encoding).
    - Ensured compatibility across different platforms and tools.
    ''')

    st.subheader('Metadata Enhancement')
    st.write('''
    - Adopted the DCAT-AP metadata standard for dataset descriptions.
    - Created metadata files in RDF format for semantic interoperability.
    - Included key metadata elements:
      - Title
      - Description
      - Publisher
      - Contact Point
      - Keywords
      - License
      - Temporal Coverage
    ''')

    st.subheader('URI and Provenance')
    st.write('''
    - Used persistent and dereferenceable URIs for datasets.
    - Documented provenance information:
      - Data sources and collection dates.
      - Processing steps and transformations.
      - Versioning information for datasets.
    ''')

    st.subheader('Tools and Technologies')
    st.write('''
    - Programming Language: Python
    - Libraries: pandas, numpy, rdflib
    - Data Visualization: Plotly, Streamlit
    - Metadata Management: DCAT-AP, RDF
    ''')

# ------------------- Sustainability Tab -------------------
with tab_sustainability:
    st.header('Sustainability of the Update of the Datasets Over Time')

    st.write('''
    This section discusses the strategies for maintaining and updating the datasets to ensure the longevity and relevance of the project.
    ''')

    st.subheader('Data Refresh Strategy')
    st.write('''
    - **Automation**:
      - Implemented scripts to automate data retrieval from sources like Eurostat.
      - Scheduled updates to check for new data releases monthly.
    - **Version Control**:
      - Utilized Git for tracking changes in data and code.
      - Tagged releases corresponding to significant data updates.
    ''')

    st.subheader('Maintenance Plan')
    st.write('''
    - **Responsibility Assignment**:
      - Designated maintainers to oversee data updates and codebase integrity.
    - **Community Engagement**:
      - Open-sourced the project to encourage contributions.
      - Provided guidelines for external collaborators.
    ''')

    st.subheader('Documentation and Support')
    st.write('''
    - Comprehensive documentation of data sources, processing steps, and methodologies.
    - User guides and contribution guidelines available in the repository.
    - Contact information provided for support and inquiries.
    ''')

    st.subheader('Long-Term Goals')
    st.write('''
    - Expand the dataset to include more countries and variables.
    - Integrate additional data sources for richer analysis.
    - Foster a community of users and contributors interested in trade data and policy analysis.
    ''')

# Optional: Provide navigation to other sections
st.write('---')
st.write('Navigate to other sections using the sidebar.')

