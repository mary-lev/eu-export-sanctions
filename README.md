# :earth_americas: The Missing Trade: Export-Import Data Discrepancies Under Sanctions Against Russia

## Overview

Since Russia's invasion of Ukraine in February 2022, the European Union (EU), alongside other international actors, implemented a series of sanctions aimed at suppressing the Russian economy. These measures were designed to limit Russia's ability to finance further aggressive actions and to pressure the government to seek peaceful resolutions. Despite these efforts, the effectiveness of the sanctions has been widely questioned. It appears that Russia has found numerous ways to circumvent these measures, often using neighboring countries to reroute its trade activities.

This project aims to verify the claims of growing trade through intermediary countries, understand the scale of potential sanctions circumvention, and explore whether these changes can be substantiated by data.
Inspiration

The project was inspired by a series of posts from Robin Brooks, where he highlighted the unusual growth of exports from EU countries to regions such as Kyrgyzstan and Armenia. Brooks' observations raised important questions:

- Is there indeed a significant growth in import and export activities involving these countries?
- How does this trade align with official data sources, including Eurostat and local data from Kyrgyzstan and Russia?

## Research Questions

What trends and changes have occurred in imports and exports to and from the EU since February 2022, particularly through intermediary countries like Kyrgyzstan and Armenia? Are these changes statistically significant, and can they be linked to the timeline of sanctions?
How well does EU data match with available open data from Kyrgyzstan and Russia? What discrepancies exist that could indicate sanctions circumvention?

## Objectives

- Detect historical baselines for trade activities
- Identify anomalous trade patterns post-2022
- Quantify the extent of trade redirection
- Analyze the role of specific intermediary countries

Focus on countries exhibiting unusual increases in trade volumes with the EU and Russia, examining their geopolitical and economic ties to assess their potential involvement in sanctions circumvention.

## Findings

Our analysis identified significant and anomalous increases in exports from the EU to certain neighboring countries post-2022:

- Kyrgyzstan: 344.8% growth
- Armenia: 148.9% growth
- Kazakhstan: 88.6% growth
- Uzbekistan: 63.8% growth
- Trinidad and Tobago: 122.6% growth

These trends are consistent with shifts in geopolitical and economic dynamics, particularly in the context of sanctions against Russia. The timing and magnitude of these trade surges, along with the geopolitical proximity and economic ties of these countries to Russia, suggest the possibility of trade redirection that may be facilitating the circumvention of EU sanctions.

## Installation

- Clone the repository

`git clone https://github.com/mary-lev/eu-export-sanctions.git`

Create and activate a virtual environment

`python -m venv venv`
`source venv/bin/activate`

- Install the required packages

`pip install -r requirements.txt`

- Run the Streamlit app

`streamlit run Home.py`

The app will automatically open in your default web browser. If not, navigate to http://localhost:8501.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Robin Brooks for the initial inspiration through his insightful observations on trade patterns.
- Data Sources: Eurostat, National statistical agencies of Kyrgyzstan, Armenia, and Russia

## Contact

For any questions or suggestions, please contact marylevchenko@gmail.com
