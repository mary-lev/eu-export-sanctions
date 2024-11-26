# pages/2_Scenario.py

import streamlit as st

# Set the page config
st.set_page_config(
    page_title='Research Context',
    page_icon='🌍',
    layout='wide'
)

# Improved sidebar
with st.sidebar:
    st.markdown('''
    ### Key Points
    - EU sanctions on Russia since February 2022
    - Unusual trade growth with neighboring states
    - Focus on export-import data discrepancies
    - Analysis of potential circumvention patterns
    ''')

# Main content
st.title('🌍 Research Context')

st.write('''
### The Challenge of Sanctions Effectiveness

Since Russia's invasion of Ukraine in February 2022, the European Union has imposed extensive sanctions aimed at limiting Russia's economic capacity. However, emerging trade patterns suggest that these measures may be less effective than intended, with evidence of systematic circumvention by neighboring countries.

### The Intermediary Countries

A clear pattern has emerged: the redirection of trade flows through intermediary countries. These countries share two key characteristics: geographical proximity to Russia and strong existing political and economic ties with Russia.

Countries such as **Kyrgyzstan** and **Armenia** have shown dramatic shifts in their trade activities since 2022. These changes are manifested in unprecedented increases in imports from EU countries and a subsequent rise in their exports to Russia.

This pattern raises significant concerns about the potential for these countries to act as channels for sanctions evasion.

### The "Missing Trade" Phenomenon

Our research focuses on a striking pattern: the emergence of significant discrepancies between:

- What EU countries report as exports to states neighboring Russia
- What these neighboring countries officially report as imports from the EU
- The subsequent flow of similar goods to Russia

> **Research Hypothesis**: The discrepancies between EU-reported exports and locally reported imports in countries neighboring Russia indicate systematic sanctions circumvention, reflected in anomalous trade data patterns post-2022.

### Research Objectives

Our research aims to:

1. **Identify Anomalous Trade Patterns Post-2022**: Track changes in trade volumes and patterns to identify statistically significant anomalies and compare pre- and post-sanctions trade flows.

2. **Establish Historical Baselines for Trade Activities**: Utilize historical trade data to establish normal trade patterns for each country, serving as a baseline for detecting anomalies.

3. **Quantify the Extent of Trade Redirection**: Measure the magnitude of increased trade flows between the EU and intermediary countries, and the subsequent flow of goods to Russia.

4. **Analyze Discrepancies Between Data Sources**: Compare Eurostat export data with local import statistics to identify inconsistencies in reported trade volumes.

5. **Assess the Role of Specific Intermediary Countries**: Investigate the roles of countries such as Kyrgyzstan and Armenia in potential sanctions circumvention.

### Research Methodology

Our investigation relies on a comprehensive comparison of data from multiple sources, including EU official statistics (Eurostat), neighboring countries' reported trade data, and Russian import/export statistics. By analyzing these datasets in parallel, we aim to identify discrepancies in reported trade volumes and track changes in trade patterns over time.

#### Data Collection

- **European Union Data**: Collected export data from **Eurostat**, covering trade flows from EU member states to non-EU countries from **2010 to 2023**.

- **Neighboring Countries' Data**: Obtained import data from the national statistical agencies of countries such as **Kyrgyzstan** and **Armenia** for the same period.

- **Russian Trade Data**: Incorporated available Russian import/export statistics, acknowledging limitations due to data restrictions post-2022.

#### Data Preparation and Standardization

- **Harmonizing Country Names**: Standardized country names across datasets to address inconsistencies (e.g., 'Kirghizistan' vs. 'Kyrgyzstan').

- **Currency Conversion**: Converted all trade values to a common currency (EUR) using historical exchange rates, adjusting for differences in units.

- **Temporal Alignment**: Aligned data on an annual basis to facilitate year-over-year comparisons.

#### Anomaly Detection

- **Trend Analysis**: Examined long-term trade trends to establish historical baselines for each country's trade activity.

- **Statistical Methods**: Calculated growth rates and utilized statistical measures (e.g., **Z-scores**) to identify significant deviations from historical norms.

- **Significance Criteria**: Focused on countries exhibiting both statistically significant growth and substantial increases in trade volumes.

---

This research aims to provide a data-driven understanding of how international trade patterns have evolved in response to sanctions, with a particular focus on the role of intermediary countries and the importance of discrepancies in export-import data.

By identifying and analyzing these anomalies, we seek to contribute to the assessment of the effectiveness of EU sanctions and offer insights that could inform policy decisions aimed at preventing sanctions circumvention.

''')
