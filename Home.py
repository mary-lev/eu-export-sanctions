import streamlit as st

# Set the page config
st.set_page_config(
    page_title='Introduction to the Project',
    page_icon=':earth_americas:',
    layout='wide'  # Optional: makes the page wide
)

# Add sidebar
with st.sidebar:
    # st.title('Introduction to the Project')
    # st.write('You are currently on: Home Page')
    
    # # Optional: Add any global filters or controls
    # st.subheader('Global Filters')
    # time_period = st.select_slider(
    #     'Select Time Period',
    #     options=['2020', '2021', '2022', '2023', '2024'],
    #     value=('2020', '2024')
    # )
    
    # # Optional: Add other controls
    # st.subheader('Data Options')
    # show_raw_data = st.checkbox('Show Raw Data Tables', value=False)
    
    # # Optional: Add some useful information
    # st.markdown('---')  # Adds a horizontal line
    st.markdown('''
    ### About
    This project analyzes trade patterns 
    between EU and intermediary countries 
    after Russia's invasion of Ukraine.
    
    ### Data Sources
    - Eurostat
    - Kyrgyzstan Statistics
    - Russian Trade Data
    ''')

st.title(':earth_americas: Introduction to the Project')

st.write('''
Since Russia's invasion of Ukraine in February 2022, the European Union, alongside other international actors, implemented a series of sanctions aimed at suppressing the Russian economy. These measures were designed to limit Russia's ability to finance further aggressive actions and to pressure the government to seek peaceful resolutions. Despite these efforts, two years later, the effectiveness of the sanctions has been widely questioned. It appears that Russia has found numerous ways to circumvent these measures, often using neighboring countries to reroute its trade activities.

One particular method involved redirecting the flow of imports and exports through intermediaries, countries that are geographically close to and economically tied with Russia. Countries like Kyrgyzstan, Armenia, and others have seen noticeable shifts in their trade activities since 2022, which led to concerns that they might be facilitating Russia's sanction evasion.

This project was inspired by a series of posts from [Robert Brooks on Twitter](https://x.com/robin_j_brooks), where he highlighted the unusual growth of exports from EU countries to these regions, notably Kyrgyzstan and Armenia. Brooks' observations raised important questions: Is there indeed a significant growth in import and export activities involving these countries? And if so, how does this trade align with official data sources, including Eurostat and local data from Kyrgyzstan and Russia?
         ''')

# Placeholder for images from Twitter

# Display images in a grid format to save space
cols = st.columns(4)

# Replace 'twitter_image_1.png', 'twitter_image_2.png', etc. with actual image paths or URLs
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

# Loop through images and display them in grid
for idx, (img_path, caption) in enumerate(images):
    cols[idx % 4].image(img_path, caption=caption, use_container_width=True)


st.write('''
The goal of this project is to verify the claims of growing trade through intermediary countries, understand the scale of potential sanction circumvention, and explore whether these changes can be substantiated by the data. We do this by examining available data on exports and imports from different sources, including the EU's official statistics (Eurostat) and, where possible, data reported by Kyrgyzstan and Russia. By comparing these datasets, we aim to uncover discrepancies, such as mismatches in reported export and import volumes, identify trends, and better understand whether these intermediary countries have become key players in helping Russia bypass economic restrictions. These discrepancies could also impact the credibility of these countries as reliable international trade partners.

The questions we explore in this project are:

- What trends and changes have occurred in imports and exports to and from the EU since February 2022, particularly through intermediary countries like Kyrgyzstan and Armenia? Are these changes statistically significant, and can they be linked to the timeline of sanctions?
- How well does EU data match with available open data from Kyrgyzstan and Russia, and what discrepancies exist that could indicate sanction circumvention?

These questions are essential to evaluate the true impact of sanctions and to determine how effective they have been in limiting Russia's economic activity. We hope that our analysis can shed light on the broader implications of these sanction policies and provide insights for policymakers.
''')


st.write('We invite you to explore the data with us and better understand how international trade has evolved in light of recent geopolitical events.')
