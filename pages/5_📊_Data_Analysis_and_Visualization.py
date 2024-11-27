import streamlit as st
import pandas as pd
import glob
import os
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title='EU Export Analysis to Russia, Kyrgyzstan, and Armenia',
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


def load_state_statistics_data(file_path):
    xl = pd.ExcelFile(file_path)
    df = xl.parse(xl.sheet_names[0], header=None)

    df_cleaned = df.iloc[2:8, 2:]

    df_cleaned.columns = ['Category'] + \
        [str(year) for year in range(1994, 2024)]

    df_cleaned = df_cleaned[df_cleaned['Category'].notna()]

    melted_df = df_cleaned.melt(
        id_vars=['Category'], var_name='Year', value_name='Value')
    melted_df['Year'] = melted_df['Year'].astype(int)

    return melted_df


def load_data(folder_path):
    combined_df = pd.DataFrame()
    for file in glob.glob(os.path.join(folder_path, '*.csv')):
        df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df


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


def preprocess_data_kazakhstan(data):
    combined_df_filtered = data[['REPORTER', 'PERIOD', 'VALUE_IN_EUR']]

    combined_df_filtered = combined_df_filtered[~combined_df_filtered['REPORTER'].str.contains(
        'Euro area|European Union')]

    combined_df_filtered['REPORTER'] = combined_df_filtered['REPORTER'].str.split(
    ).str[0]

    combined_df_filtered['PERIOD'] = pd.to_datetime(
        combined_df_filtered['PERIOD'].str.split('-').str[0], format='%Y%m', errors='coerce')

    combined_df_filtered['PERIOD'] = combined_df_filtered['PERIOD'].dt.strftime(
        '%Y-%m')

    combined_df_filtered = combined_df_filtered.sort_values(by='PERIOD')

    return combined_df_filtered


def preprocess_data_uzbekistan(filename):
    uzbekistan_state_data = pd.read_csv(filename)
    uzbekistan_long = uzbekistan_state_data.melt(
        id_vars=['Code', 'Klassifikator_en'],
        value_vars=[str(year) for year in range(2010, 2024)],
        var_name='Year',
        value_name='Import Value'
    )
    uzbekistan_long['Year'] = uzbekistan_long['Year'].astype(int)
    return uzbekistan_long


def main():
    st.title('EU Export Analysis to Russia, Kyrgyzstan, and Armenia')

    st.write('''
    This analysis aims to answer the question: **How well does EU data match with available open data from Kyrgyzstan and Russia, and what discrepancies exist that could indicate sanction circumvention?**

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

    kyrgyzstan_state_stats = load_state_statistics_data(
        'data/kyrgyzstan_data/4.03.00.20 Географическое распределение импорта товаров..xlsx')
    uzbekistan_state_stats = preprocess_data_uzbekistan('data/uzbekistan_data/sdmx_data_1176.csv')

    tab_russia, tab_kyrgyzstan, tab_armenia, tab_kazakhstan, tab_uzbekistan, tab_overall_trends = st.tabs([
        'Russia',
        'Kyrgyzstan',
        'Armenia',
        'Kazakhstan',
        'Uzbekistan',
        'Overall Trends'])

    with tab_russia:
        combined_df_filtered = preprocess_data(data_russia)
        visualize_stacked_bar_chart(combined_df_filtered, 'Russia')

    with tab_kyrgyzstan:
        st.write('''
        The data below illustrates the overall export from the EU to Kyrgyzstan on a monthly basis. We also include a comparison with data from Kyrgyzstan's state statistics.
        This helps us identify any significant differences in reported values between Eurostat and [Kyrgyzstan's local records](https://stat.gov.kg/ru/statistics/vneshneekonomicheskaya-deyatelnost/).
        ''')
        combined_df_filtered = preprocess_data(data_kyrgyzstan)
        visualize_stacked_bar_chart(combined_df_filtered, 'Kyrgyzstan')

        # Visualize state statistics data
        if not kyrgyzstan_state_stats.empty:
            fig = px.line(
                kyrgyzstan_state_stats,
                x='Year',
                y='Value',
                color='Category',
                title='Total Import to Kyrgyzstan (Kyrgyzstan State Statistics Data) 1994 - 2023',
                labels={'Year': 'Year', 'Value': 'Value in Thousand US Dollars'},
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No state statistics data available for Kyrgyzstan")

        # Comparison Table: Eurostat vs Kyrgyzstan State Data
        st.subheader('Yearly Comparison of Eurostat and Kyrgyzstan State Data')
        st.write('''
        The table below provides a yearly comparison of the total export values from the EU to Kyrgyzstan as reported by Eurostat versus the values recorded by Kyrgyzstan's state statistics.

        Since 2022, there has been a significant discrepancy between the two data sources. Possible reasons for this difference include rerouting of imports to avoid sanctions, underreporting by Kyrgyzstan, differences in reporting standards, and issues with currency conversion.
        ''')
        # Filter Eurostat data to get rows for "European Union - 27 countries"
        eu_27_data = data_kyrgyzstan[data_kyrgyzstan['REPORTER'].str.contains(
            'European Union - 27 countries')]
        eu_27_data['Year'] = pd.to_datetime(
            eu_27_data['PERIOD'], format='%b. %Y').dt.year
        yearly_eu_27_data = eu_27_data.groupby(
            'Year')['VALUE_IN_EUR'].sum().reset_index()
        yearly_eu_27_data.rename(
            columns={'VALUE_IN_EUR': 'Eurostat Value (EUR)'}, inplace=True)
        yearly_eu_27_data['Year'] = yearly_eu_27_data['Year'].astype(str)

        # Merge with Kyrgyzstan state data for comparison
        kyrgyz_total = kyrgyzstan_state_stats[kyrgyzstan_state_stats['Category'] == 'The EU'][[
            'Year', 'Value']]
        kyrgyz_total.rename(
            columns={'Value': 'Kyrgyzstan State Value (Thousand USD)'}, inplace=True)
        kyrgyz_total['Year'] = kyrgyz_total['Year'].astype(str)
        comparison_df = pd.merge(
            yearly_eu_27_data, kyrgyz_total, on='Year', how='inner').set_index('Year')
        # Add a new column to calculate the percentage difference
        comparison_df['Percentage Difference (%)'] = (
            (comparison_df['Eurostat Value (EUR)'] - comparison_df['Kyrgyzstan State Value (Thousand USD)'] * 1000) / comparison_df['Eurostat Value (EUR)']) * 100

        # Display the comparison table
        st.dataframe(comparison_df)

        st.write('''
        The significant difference starting from 2022 between Eurostat and Kyrgyzstan's state data could be due to several reasons:

        - Re-Routing and Sanctions Evasion: After sanctions were implemented, Russia likely rerouted many of its imports through countries like Kyrgyzstan, possibly using other transit routes to avoid detection and sanctions. This would cause a sudden surge in reported trade in the Eurostat data compared to local data that may not capture these re-export activities fully.
        - Underreporting by Kyrgyzstan: The Kyrgyz government might not have fully recorded or may have chosen not to report certain import activities in detail. This could be due to administrative challenges, informal trade activities, or political considerations—especially if these activities are seen as a way to avoid international sanctions.
        - Delayed or Limited Data: Local Kyrgyzstan statistics might have delays or limitations in capturing the entire breadth of trade activities accurately. It’s possible that the trade data collection processes and infrastructure are less sophisticated compared to the EU's standards, leading to discrepancies.
        - Different Reporting Standards: Eurostat uses harmonized methodologies that ensure consistency across EU countries. On the other hand, Kyrgyzstan’s data might be based on different classifications, accounting practices, or even exchange rate calculations, leading to differences.
        - Currency Valuation and Conversion Issues: The values are in EUR and USD, which introduces potential discrepancies due to exchange rate fluctuations. The timing of data collection and currency conversion can also significantly impact the reported numbers.
        - Sanctioned Goods and Parallel Trade: There might be discrepancies specifically for sanctioned goods that Kyrgyzstan prefers to keep off-record. This could involve sensitive items like technology or dual-use goods, which may be routed through Kyrgyzstan to reach Russia.

        These differences suggest a need to critically analyze both data sources, especially considering the political and economic pressures at play during and after the imposition of sanctions on Russia.
                 ''')

    with tab_armenia:
        combined_df_filtered = preprocess_data(data_armenia)
        visualize_stacked_bar_chart(combined_df_filtered, 'Armenia')
        armenia_state_file_path = 'data/armenia_data/armenia_data.csv' 
        armenia_state_data = pd.read_csv(armenia_state_file_path)
        armenia_state_data = armenia_state_data.rename(columns={
            'country': 'REPORTER',
            'year': 'YEAR',
        })
        armenia_state_data = armenia_state_data[armenia_state_data['timeperiod'] == 'Year']
        armenia_state_data['YEAR'] = armenia_state_data['YEAR'].astype(int)

        armenia_eurostat = data_armenia
        armenia_eurostat['YEAR'] = armenia_eurostat['PERIOD'].str.extract(r'(\d{4})').astype(int)
        armenia_eurostat_grouped = armenia_eurostat.groupby(['REPORTER', 'YEAR'])['VALUE_IN_EUR'].sum().reset_index()
        print(armenia_eurostat_grouped.columns)

        comparison_data = pd.merge(
            armenia_eurostat_grouped,
            armenia_state_data,
            on=['REPORTER', 'YEAR'],
            how='inner',
            suffixes=('_Eurostat', '_State')
        )
        comparison_data = comparison_data[['REPORTER', 'YEAR', 'VALUE_IN_EUR', 'import_consigment', 'import_origin']].copy()
        comparison_data["import_consigment"] = comparison_data["import_consigment"].replace('-', np.nan)

        # Convert the column to float and handle NaN values
        comparison_data["import_consigment"] = comparison_data["import_consigment"].astype(float)

        # Multiply by 1000 to convert from thousands to dollars
        comparison_data["import_consigment"] *= 1000

        st.dataframe(comparison_data)

    with tab_kazakhstan:
        data_kazakhstan = load_data('data/kazahstan_export_eurostat')
        combined_df_filtered = preprocess_data_kazakhstan(data_kazakhstan)
        visualize_stacked_bar_chart(combined_df_filtered, 'Kazakhstan')

    with tab_uzbekistan:
        combined_df_filtered = preprocess_data(data_uzbekistan)
        visualize_stacked_bar_chart(combined_df_filtered, 'Uzbekistan')

        data_uzbekistan['YEAR'] = data_uzbekistan['PERIOD'].str.extract(r'(\d{4})').astype(int)
        grouped_df = data_uzbekistan.groupby(['REPORTER', 'YEAR'])['VALUE_IN_EUR'].sum().reset_index()
        grouped_df['REPORTER'] = grouped_df['REPORTER'].str.split().str[0]

        uzbekistan_state_stats['YEAR'] = uzbekistan_state_stats['Year'].astype(int)
        uzbekistan_state_stats["Import Value"] = uzbekistan_state_stats["Import Value"].astype(float)
        uzbekistan_state_stats["Import Value"] *= 1000
        uzbekistan_state_stats.rename(columns={'Klassifikator_en': 'REPORTER', "Import Value": "Import Value, in USD"}, inplace=True)

        merged_data_reporter = pd.merge(
            grouped_df, 
            uzbekistan_state_stats, 
            on=['REPORTER', 'YEAR'], 
            how='inner', 
            suffixes=('_export', '_import')
        )

        st.write('''
                 Combined Eurostat data about EU export to Uzbekistan and Uzbekistan state import data from EU
                    ''')
        st.dataframe(merged_data_reporter)

    with tab_overall_trends:
        combined_data = []
        countries = ['Russia', 'Kyrgyzstan', 'Armenia',
            'Kazakhstan', 'Uzbekistan']
        data_files = [data_russia, data_kyrgyzstan, data_armenia,
            data_kazakhstan, data_uzbekistan]
        preprocess_funcs = [preprocess_data, preprocess_data, preprocess_data,
            preprocess_data_kazakhstan, preprocess_data]

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
        fig.update_layout(barmode='stack')

        st.plotly_chart(fig, use_container_width=True)


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
