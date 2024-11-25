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

Since Russia's invasion of Ukraine in February 2022, the European Union has imposed extensive sanctions to 
to limit Russia's economic capacity. However, emerging trade patterns suggest that these measures may be 
less effective than intended, with evidence of systematic circumvention by neighbouring states.
         
### The Intermediary Countries

A clear pattern has emerged: the redirection of trade flows through intermediary countries. 
These countries share two key characteristics: geographical proximity to Russia 
and strong existing political and economic ties with Russia.

Countries such as **Kyrgyzstan** and **Armenia** show dramatic shifts in their trade activities since 2022. 
These changes are manifested in unprecedented increases in imports from EU countries and subsequent growth in their trade with Russia.

This pattern raises significant concerns about the potential for these countries to act as channels for sanctions evasion.

### The "Missing Trade" Phenomenon

Our research focuses on a striking pattern: the emergence of significant discrepancies between:
- What EU countries report as exports to states neighboring Russia
- What these countries officially report as imports from the EU
- The subsequent flow of similar goods to Russia

> **Research Hypothesis**: The discrepancies between EU-reported exports and locally-reported imports in 
countries neighboring Russia indicate systematic sanctions circumvention, reflected in anomalous trade data patterns post-2022.

### Research Methodology

Our investigation relies on comprehensive data comparison across multiple sources:
- EU's official statistics (Eurostat)
- Kyrgyzstan's reported trade data
- Russian import/export statistics

By analyzing these datasets in parallel, we aim to:
1. Identify discrepancies in reported trade volumes
2. Track changes in trade patterns over time
3. Map the flow of goods through intermediary countries
         
### Research Objectives

1. **Data Pattern Analysis**
   - Track changes in trade volumes and patterns
   - Identify statistically significant anomalies
   - Compare pre and post-sanctions trade flows

2. **Source Comparison**
   - Analyze Eurostat export data
   - Examine local import statistics
   - Map discrepancies between data sources

3. **Impact Assessment**
   - Evaluate the scale of potential circumvention
   - Assess implications for sanctions effectiveness
   - Identify patterns requiring further investigation

### Why This Matters

Understanding these trade patterns is crucial for:
- Evaluating sanctions effectiveness
- Identifying potential circumvention mechanisms
- Informing policy adjustments
- Maintaining international trade integrity

### Key Stakeholders

- **Policy Makers**: Need evidence-based insights for sanction adjustments
- **Trade Regulators**: Require data on potential circumvention patterns
- **Research Community**: Seeks to understand sanctions effectiveness
- **International Organizations**: Monitor trade compliance

---

This research aims to provide a data-driven understanding of how international trade patterns 
         have evolved in response to have evolved in response to sanctions, with a particular focus 
         on the role of intermediary countries and the importance of the differences in export-import data.
''')