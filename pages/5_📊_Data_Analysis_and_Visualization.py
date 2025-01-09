import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title='EU Export Analysis to Russia, Kyrgyzstan, Uzbekistan, Kazakhstan, and Armenia',
    page_icon=':bar_chart:',
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
    ''')

exchange_rates = {
    2019: 1.12,
    2020: 1.14,
    2021: 1.18,
    2022: 1.05,
    2023: 1.07
}

def parse_period_to_year(period: str) -> int:
    """Parse different period formats to extract year"""
    try:
        return int(period.split()[-1])
    except Exception:
        return None

def load_national_data():
    """Load converted national statistics data"""
    national_data = {}
    
    # Load each country's converted data
    try:
        national_data['kyrgyzstan'] = pd.read_csv('data/national_data_converted/kyrgyz_import_yearly.csv')
        national_data['armenia'] = pd.read_csv('data/national_data_converted/armenia_import_yearly.csv')
        national_data['kazakhstan'] = pd.read_csv('data/national_data_converted/kazakhstan_import_yearly.csv')
        national_data['uzbekistan'] = pd.read_csv('data/national_data_converted/uzbek_import_yearly.csv')
    except Exception as e:
        st.error(f"Error loading national data: {e}")
        return {}
    
    return national_data


def load_data(folder_path):
    combined_df = pd.DataFrame()
    for file in glob.glob(os.path.join(folder_path, '*.csv')):
        df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df


def compare_eurostat_national(eurostat_data: pd.DataFrame, national_data: pd.DataFrame, 
                            country_name: str) -> pd.DataFrame:
    """Compare Eurostat and national data"""
    
    # Extract yearly data from Eurostat
    print(eurostat_data.head())
    eurostat_yearly = eurostat_data[eurostat_data['REPORTER'].str.contains(
        'European Union - 27 countries')].copy()
    eurostat_yearly['Year'] = pd.to_datetime(
        eurostat_yearly['PERIOD'], format='%b. %Y').dt.year
    print(eurostat_yearly.head())

    eurostat_yearly = eurostat_yearly.groupby('Year')['VALUE_IN_EUR'].sum().reset_index()
    print(eurostat_yearly.head())
    
    # Get national data
    national_yearly = national_data[national_data['PARTNER'].str.contains(
        'European Union - 27 countries')].copy()
    national_yearly['Year'] = national_yearly['PERIOD'].str.extract(r'Y(\d{4})').astype(int)
    
    # Merge data
    comparison = pd.merge(
        eurostat_yearly, 
        national_yearly,
        on='Year',
        suffixes=('_eurostat', '_national')
    )
    
    # Calculate discrepancy
    comparison['Discrepancy'] = comparison['VALUE_IN_EUR_eurostat'] - comparison['VALUE_IN_EUR_national']
    comparison['Discrepancy_Percentage'] = (
        comparison['Discrepancy'] / comparison['VALUE_IN_EUR_eurostat'] * 100
    ).round(2)
    
    return comparison

def preprocess_data(data):
    combined_df_filtered = data[['REPORTER', 'PERIOD', 'VALUE_IN_EUR']]

    # Remove rows where 'REPORTER' contains 'Euro area' or 'European Union'
    combined_df_filtered = combined_df_filtered[~combined_df_filtered['REPORTER'].str.contains(
        'Euro area|European Union|Union européenne|Zone euro')]

    combined_df_filtered['REPORTER'] = combined_df_filtered['REPORTER'].str.split(
    ).str[0]

    combined_df_filtered['PERIOD'] = pd.to_datetime(
        combined_df_filtered['PERIOD'], format='%b. %Y', errors='coerce')

    combined_df_filtered['PERIOD'] = combined_df_filtered['PERIOD'].dt.strftime(
        '%Y-%m')

    combined_df_filtered = combined_df_filtered.sort_values(by='PERIOD')

    return combined_df_filtered


def display_country_comparison(tab, eurostat_data, national_data, country_name):
    """Display comparison for a specific country"""
    
    # Regular Eurostat visualization
    combined_df_filtered = preprocess_data(eurostat_data)
    visualize_stacked_bar_chart(combined_df_filtered, country_name)
    
    # National data comparison
    st.write(f"""
    ### Comparison of Eurostat and {country_name} National Statistics
    The data below compares export values reported by Eurostat with import values from {country_name}'s national statistics.
    Both datasets have been converted to EUR for direct comparison.
    """)
    
    comparison_df = compare_eurostat_national(eurostat_data, national_data, country_name)
    comparison_df["IMPORTER"] = country_name
    comparison_df["EXPORTER"] = "EU"
    comparison_df["Discrepancy, EUR"] = comparison_df["Discrepancy"]
    comparison_df["Discrepancy, %"] = comparison_df["Discrepancy_Percentage"]
    comparison_df["Eurostat Data, EUR"] = comparison_df["VALUE_IN_EUR_eurostat"]
    comparison_df["National Data, EUR"] = comparison_df["VALUE_IN_EUR_national"]
    table_columns = ['Year', 'IMPORTER', 'EXPORTER', 'Eurostat Data, EUR', 'National Data, EUR',
       'Discrepancy, EUR', 'Discrepancy, %']
    table = comparison_df[table_columns].copy()

    st.dataframe(table)
    
    # Visualize discrepancies
    fig = px.bar(
        comparison_df,
        x='Year',
        y='Discrepancy_Percentage',
        title=f'Discrepancies between Eurostat and {country_name} Data (%)',
        labels={'Discrepancy_Percentage': 'Discrepancy %', 'Year': 'Year'}
    )
    
    # # Add war start marker
    # fig.add_vline(
    #     x=2022,
    #     line_dash="dash",
    #     line_color="red",
    #     annotation_text="War Start (2022)",
    #     annotation_position="top"
    # )
    
    st.plotly_chart(fig)
    
    # Analysis text
    if comparison_df['Year'].max() >= 2022:
        pre_war_avg = comparison_df[comparison_df['Year'] < 2022]['Discrepancy_Percentage'].mean()
        post_war_avg = comparison_df[comparison_df['Year'] >= 2022]['Discrepancy_Percentage'].mean()
        
        st.write(f"""
        **Key Observations:**
        - Average discrepancy before 2022: {pre_war_avg:.2f}%
        - Average discrepancy from 2022 onwards: {post_war_avg:.2f}%
        - Change in discrepancy: {post_war_avg - pre_war_avg:.2f} percentage points
        
        {f"The discrepancy {'increased' if post_war_avg > pre_war_avg else 'decreased'} significantly after the start of the war, " if abs(post_war_avg - pre_war_avg) > 10 else "The discrepancy remained relatively stable after the start of the war, "}
        which could indicate {'potential trade flow changes' if abs(post_war_avg - pre_war_avg) > 10 else 'consistent reporting practices'}.
        """)



def main():
    st.title('EU Export Analysis to Russia, Kyrgyzstan, Kazakhstan, Uzbekistan, and Armenia')

    st.write('''
    This analysis aims to answer the question: **How well does EU data match with available open data from Kyrgyzstan, Uzbekistan, Kazakhstan, and Armenia, and what discrepancies exist that could indicate sanction circumvention?**

    After the onset of sanctions on Russia due to the invasion of Ukraine, there have been significant shifts in trade patterns involving intermediary countries like Kyrgyzstan, Armenia. By analyzing trade data from 2019 to 2024, we seek to:
    - Determine whether there has been an increase in exports from the EU to these intermediary countries.
    - Compare Eurostat's export data to local statistics.
    - Highlight discrepancies in reported trade values that could suggest efforts to circumvent international sanctions.

    Use the tabs to navigate between different countries to view detailed analyses of the trade data.
    '''
             )
    data_russia = load_data('data/russia_export_eurostat')
    data_kyrgyzstan = load_data('data/kyrgyz_export_eurostat')
    data_armenia = load_data('data/armenia_export_eurostat')
    data_uzbekistan = load_data('data/uzbek_export_eurostat')
    data_kazakhstan = load_data('data/kazakhstan_export_eurostat')

    national_data = load_national_data()

    tab_kyrgyzstan, tab_armenia, tab_kazakhstan, tab_uzbekistan, tab_russia, tab_overall_trends = st.tabs([
        'Kyrgyzstan',
        'Armenia',
        'Kazakhstan',
        'Uzbekistan',
        "Russia",
        'Overall Trends'])

    with tab_kyrgyzstan:
        if 'kyrgyzstan' in national_data:
            display_country_comparison(tab_kyrgyzstan, data_kyrgyzstan, 
                                    national_data['kyrgyzstan'], 'Kyrgyzstan')
    
    with tab_armenia:
        if 'armenia' in national_data:
            display_country_comparison(tab_armenia, data_armenia, 
                                    national_data['armenia'], 'Armenia')
    
    with tab_kazakhstan:
        if 'kazakhstan' in national_data:
            display_country_comparison(tab_kazakhstan, data_kazakhstan, 
                                    national_data['kazakhstan'], 'Kazakhstan')
    
    with tab_uzbekistan:
        if 'uzbekistan' in national_data:
            display_country_comparison(tab_uzbekistan, data_uzbekistan, 
                                    national_data['uzbekistan'], 'Uzbekistan')

    with tab_russia:
        combined_df_filtered = preprocess_data(data_russia)
        visualize_stacked_bar_chart(combined_df_filtered, 'Russia')

    with tab_overall_trends:
        combined_data = []
        countries = ['Russia', 'Kyrgyzstan', 'Armenia',
            'Kazakhstan', 'Uzbekistan']
        data_files = [data_russia, data_kyrgyzstan, data_armenia,
            data_kazakhstan, data_uzbekistan]
        preprocess_funcs = [preprocess_data, preprocess_data, preprocess_data,
            preprocess_data, preprocess_data]

        for country, data, preprocess in zip(countries, data_files, preprocess_funcs):
            preprocessed_data = preprocess(data)
            monthly_data = preprocessed_data.groupby(
                'PERIOD')['VALUE_IN_EUR'].sum().reset_index()
            monthly_data.rename(
                columns={'VALUE_IN_EUR': 'Export Value', 'PERIOD': 'Month'}, inplace=True)
            monthly_data['Country'] = country
            combined_data.append(monthly_data)

        combined_df = pd.concat(combined_data, ignore_index=True)

        fig = px.bar(
            combined_df,
            x='Month',
            y='Export Value',
            color='Country',
            title='Overall Export Trends from EU to Russia, Kyrgyzstan, Armenia, Uzbekistan, and Kazakhstan (2019 - 2024)',
            labels={'Month': 'Month',
                'Export Value': 'Export Value (EUR)', 'Country': 'Country'}
        )

        feb_2022 = pd.Timestamp('2022-02-01')
        fig.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=feb_2022,
                    x1=feb_2022,
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    line=dict(color="red", width=2, dash="dash")
                )
            ],
            annotations=[
                dict(
                    x=feb_2022,
                    y=1,
                    xref="x",
                    yref="paper",
                    showarrow=False,
                    text="Feb 2022",
                    align="center"
                )
            ]
        )
        fig.update_layout(barmode='stack')

        st.plotly_chart(fig, use_container_width=True)

        st.write('''
            Based on the overall export trends visualized in the chart, it is evident that there was a significant increase in exports to countries like Kazakhstan, Kyrgyzstan, Armenia, and Uzbekistan after 2022, coinciding with the start of the war and the imposition of sanctions on Russia. This suggests that these countries may have played a role as intermediaries, potentially rerouting goods to Russia to circumvent sanctions.

            However, despite this noticeable growth in exports to these neighboring countries, the decrease in exports directly to Russia remains substantial and is not fully offset by the increases elsewhere. This implies that the overall export volume from the EU to this region experienced a net decline rather than full compensation. This trend underscores the impact of geopolitical changes on trade dynamics and highlights the need for a closer examination of re-routing practices and their implications for regional trade policies.
        ''')


def visualize_stacked_bar_chart(data, country_name):
    data['PERIOD'] = pd.to_datetime(data['PERIOD'], format='%Y-%m', errors='coerce')

    grouped_df = data.groupby(['PERIOD', 'REPORTER'])['VALUE_IN_EUR'].sum().reset_index()

    if not grouped_df.empty:
        fig = px.bar(
            grouped_df,
            x='PERIOD',
            y='VALUE_IN_EUR',
            color='REPORTER',
            title=f'Exports to {country_name} from EU Countries (2019 - 2024) / EuroStat Data',
            labels={'VALUE_IN_EUR': 'Value in EUR', 'PERIOD': 'Month', 'REPORTER': 'Country'},
        )

        feb_2022 = pd.Timestamp('2022-02-01')
        fig.update_layout(
            shapes=[
                dict(
                    type="line",
                    x0=feb_2022,
                    x1=feb_2022,
                    y0=0,
                    y1=1,
                    xref="x",
                    yref="paper",
                    line=dict(color="red", width=2, dash="dash")
                )
            ],
            annotations=[
                dict(
                    x=feb_2022,
                    y=1,
                    xref="x",
                    yref="paper",
                    showarrow=False,
                    text="Feb 2022",
                    align="center"
                )
            ]
        )

        fig.update_layout(barmode='stack', xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(f"No data available for exports to {country_name}")



if __name__ == "__main__":
    main()
