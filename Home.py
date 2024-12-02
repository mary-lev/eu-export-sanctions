import streamlit as st

st.set_page_config(
    page_title='Introduction to the Project',
    page_icon=':earth_americas:',
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
                

    _The code and data for this project is available on [GitHub](https://github.com/mary-lev/eu-export-sanctions)._

    _[Maria Levchenko](mailto:marylevchenko@gmail.com), 2024_
    ''')
     
st.title(':earth_americas: The Missing Trade: Export-Import Data Discrepancies Under Sanctions Against Russia')

st.write('''
        Since Russia's invasion of Ukraine in February 2022, the European Union, alongside other international actors, 
         implemented a series of sanctions aimed at suppressing the Russian economy. 
         These measures were designed to limit Russia's ability to finance further aggressive actions and 
         to pressure the government to seek peaceful resolutions. Despite these efforts, two years later, 
         the effectiveness of the sanctions has been widely questioned. It appears that Russia has found numerous ways 
         to circumvent these measures, often using neighboring countries to reroute its trade activities.
       
        This project was inspired by a series of posts from [Robert Brooks on Twitter](https://x.com/robin_j_brooks), 
         where he highlighted the unusual growth of exports from EU countries to these regions, notably Kyrgyzstan and Armenia. 
         Brooks' observations raised important questions: Is there indeed a significant growth in import and export activities 
         involving these countries? And if so, how does this trade align with official data sources, 
         including Eurostat and local data from Kyrgyzstan and Russia?
    ''')

cols = st.columns(4)
images = [
        ('images/1.png', 'Growth of Exports from Germany to Kyrgyzstan'),
        ('images/2.png', 'Growth of Exports from Germany to other countries'),
        ('images/3.png', 'Growth of Exports from EU to Kyrgyzstan (1)'),
        ('images/4.png', 'Growth of Exports from EU to Kyrgyzstan (2)'),
        ('images/5.png', 'Dutch and Belgian exports to Kyrgyzstan'),
        ('images/6.png', 'Italian Exports to Kyrgyzstan and Armenia'),
        ('images/7.png', 'France Exports to Kyrgyzstan'),
        ('images/8.png', 'Growth of Exports from EU to Kyrgyzstan'),
    ]

for idx, (img_path, caption) in enumerate(images):
    cols[idx % 4].image(img_path, caption=caption, use_container_width=True)

st.write('''
    The goal of this project is to verify the claims of growing trade through intermediary countries, 
         understand the scale of potential sanction circumvention, and explore whether 
         these changes can be substantiated by the data. 

    ### Research Questions:

    - What trends and changes have occurred in imports and exports to and from the EU since February 2022, 
         particularly through intermediary countries like Kyrgyzstan and Armenia? 
         Are these changes statistically significant, and can they be linked to the timeline of sanctions?
    - How well does EU data match with available open data from Kyrgyzstan, Armenia, Uzbekistan, Kazakhstan and Russia, 
         and what discrepancies exist that could indicate sanction circumvention?
    
    ### Research Hypothesis
    After the implementation of EU sanctions in February 2022, there are anomalous trade patterns and a systematic pattern of "missing trade" for some EU trading partners where:

    - Independent variable: Time period (pre vs. post February 2022 sanctions)

    - Dependent variables:
        - Year-over-year growth rates of EU exports to some countries
        - Trade volume thresholds (minimum 100 million EUR in 2022)
        - Statistical significance measures:
            - Z-scores of growth rates (relative to 2010-2021 baseline)
            - Standard deviations from historical means

    - Expected relationships:
        1. Statistical significance: Growth rates will show Z-scores > 1.96 (95% confidence level)
        2. Magnitude: Year-over-year growth rates will exceed 50% compared to historical averages
        3. Volume significance: Export volumes will exceed 100 million EUR in 2022
        4. Geographic pattern: These anomalies will be concentrated in countries with:
            - Geographic proximity to Russia
            - Established economic ties with both EU and Russia
        5. Discrepancy patterns: The gap between EU-reported exports and partner-reported imports will increase significantly post-sanctions. 

    - Control metrics:
        - Historical baseline (2010-2021) mean growth rates
        - Standard deviation of historical growth rates
        - Pre-sanctions trade volumes and discrepancy levels
    
    By identifying and analyzing these anomalies, we seek to contribute to the assessment of the effectiveness of EU sanctions and offer insights that could inform policy decisions aimed at preventing sanctions circumvention.

    ''')
