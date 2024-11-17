# pages/2_Scenario.py

import streamlit as st

# Set the page config
st.set_page_config(
    page_title='Scenario',
    page_icon='🌍',
    layout='wide'
)

# Add sidebar
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
st.title('🌍 Scenario')

st.write('''
## Background

Since Russia's invasion of Ukraine in February 2022, the European Union, along with other international actors, has implemented a series of sanctions aimed at crippling the Russian economy. These sanctions are intended to limit Russia's ability to finance its military operations and to pressure the government to seek peaceful resolutions.

However, concerns have arisen regarding the effectiveness of these sanctions. Evidence suggests that Russia may be circumventing these measures by rerouting its trade through neighboring countries. Nations like **Kyrgyzstan**, **Armenia**, **Georgia**, and **Kazakhstan** have experienced unusual increases in trade volumes with EU countries, indicating they might be acting as intermediaries.

## Hypothesis

This project hypothesizes that **Russia is circumventing EU sanctions by increasing trade through intermediary countries such as Kyrgyzstan and Armenia**, which is reflected in anomalous trade data patterns post-2022.

## Objectives

- **Analyze Trade Data**: Examine import and export data from Eurostat and local statistics to identify trends and anomalies in trade patterns with intermediary countries.
- **Identify Discrepancies**: Compare EU data with data from Kyrgyzstan and Russia to uncover any discrepancies that may indicate sanction circumvention.
- **Assess Impact**: Evaluate the effectiveness of the sanctions and the potential economic and political implications of these trade patterns.

## Importance of the Study

Understanding how sanctions are being circumvented is crucial for:

- **Policy Enforcement**: Enhancing the effectiveness of sanctions and closing loopholes.
- **International Relations**: Maintaining the integrity of international trade agreements.
- **Economic Stability**: Preventing unfair trade practices that can distort markets.

## Stakeholders

- **European Union Policymakers**: Responsible for implementing and enforcing sanctions.
- **Intermediary Countries**: Potentially facilitating trade between the EU and Russia.
- **Global Trade Community**: Interested in fair trade practices and compliance.
- **Researchers and Analysts**: Studying the geopolitical and economic impacts of sanctions.

---

We invite you to explore the data and analyses presented in this project to gain a deeper understanding of the evolving international trade dynamics in light of recent geopolitical events.
''')
