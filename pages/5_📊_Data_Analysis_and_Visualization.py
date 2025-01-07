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
    data_kazakhstan = load_data('data/kazahstan_export_eurostat')

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
        st.subheader('Yearly Comparison of Eurostat and Kyrgyzstan State Data (Converted to USD)')
        st.write('''
        The table below provides a yearly comparison of the total export values from the EU to Kyrgyzstan as reported by Eurostat versus the values recorded by Kyrgyzstan's state statistics.

        Since 2022, there has been a significant discrepancy between the two data sources. Possible reasons for this difference include rerouting of imports to avoid sanctions, underreporting by Kyrgyzstan, differences in reporting standards, and issues with currency conversion.
        ''')
        # Filter Eurostat data to get rows for "European Union - 27 countries"
        eu_27_data = data_kyrgyzstan[data_kyrgyzstan['REPORTER'].str.contains(
            'European Union - 27 countries')]
        eu_27_data['Year'] = pd.to_datetime(
            eu_27_data['PERIOD'], format='%b. %Y').dt.year
        eu_27_data['exchange_rate'] = eu_27_data['Year'].astype(int).map(exchange_rates)
        eu_27_data['Eurostat Value (USD)'] = eu_27_data['VALUE_IN_EUR'] * eu_27_data['exchange_rate']

        yearly_eu_27_data = eu_27_data.groupby(
            'Year')['Eurostat Value (USD)'].sum().reset_index()
        yearly_eu_27_data['Year'] = yearly_eu_27_data['Year'].astype(str)
        st.dataframe(yearly_eu_27_data)

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
            (comparison_df['Eurostat Value (USD)'] - comparison_df['Kyrgyzstan State Value (Thousand USD)'] * 1000) / comparison_df['Eurostat Value (USD)']) * 100

        st.dataframe(comparison_df)

        st.write('''
            **Key Observations**:
            - Eurostat values have been converted to USD for consistency with Kyrgyzstan's state data.
            - Post-2022, discrepancies surged, likely due to rerouting of trade through Kyrgyzstan amidst sanctions on Russia.
            - Differences may also stem from reporting standards, underreporting, or unrecorded sensitive goods.
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
        armenia_eurostat['REPORTER'] = armenia_eurostat['REPORTER'].str.split().str[0]
        armenia_eurostat['YEAR'] = armenia_eurostat['PERIOD'].str.extract(r'(\d{4})').astype(int)
        armenia_eurostat_grouped = armenia_eurostat.groupby(['REPORTER', 'YEAR'])['VALUE_IN_EUR'].sum().reset_index()

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
        comparison_data["import_origin"] = comparison_data["import_origin"].replace('-', np.nan)
        comparison_data["import_origin"] = comparison_data["import_origin"].astype(float)
        comparison_data["import_origin"] *= 1000

        comparison_data['exchange_rate'] = comparison_data['YEAR'].map(exchange_rates)

        # Convert EU export values to USD
        comparison_data['VALUE_IN_USD'] = comparison_data['VALUE_IN_EUR'] * comparison_data['exchange_rate']
        # Recalculate discrepancies in USD
        comparison_data['discrepancy_origin'] = comparison_data['import_origin'] - comparison_data['VALUE_IN_USD']
        comparison_data['percentage_diff_origin'] = (comparison_data['discrepancy_origin'] / comparison_data['VALUE_IN_USD']) * 100

        st.write('''
                    ### Combined Eurostat data about EU export to Armenia and Armenia state import data from EU
                The data highlights discrepancies between values reported by EU countries and Armenia. 
                Armenia provides two different metrics for imports:

                - **Consignment Value**: Reflects the value of goods based on the country from which they were dispatched.
                - **Origin Value**: Represents the value of goods based on the country where they were produced or manufactured.
    
                This distinction may contribute to differences between reported values and should be considered when interpreting the results.
        ''')

        st.dataframe(comparison_data)

        # Filter rows with significant discrepancies (absolute percentage difference > 10%)
        significant_discrepancies_new = comparison_data[(comparison_data['percentage_diff_origin'].abs() > 10)]

        country_discrepancies_origin = significant_discrepancies_new.sort_values(by='discrepancy_origin', ascending=False)
        average_discrepancies = country_discrepancies_origin.groupby('REPORTER')['discrepancy_origin'].sum().reset_index()
        average_discrepancies = average_discrepancies.sort_values(by='discrepancy_origin', ascending=False)

        # Create a bar chart for discrepancies based on origin using Plotly Express
        fig = px.bar(
            average_discrepancies,
            x='REPORTER',
            y='discrepancy_origin',
            title='Average Export-Import Discrepancies (Origin) by EU Country',
            labels={'REPORTER': 'EU Country', 'discrepancy_origin': 'Average Discrepancy (USD)'},
            color='discrepancy_origin',
            color_continuous_scale='Oranges'
        )
        # Customize the layout for better readability
        fig.update_layout(
            xaxis_title='EU Country',
            yaxis_title='Average Discrepancy (USD)',
            xaxis_tickangle=45,
            xaxis_tickmode='linear',
            yaxis=dict(title='Average Discrepancy (USD)', gridcolor='lightgrey'),
            plot_bgcolor='white'
        )

        st.plotly_chart(fig, use_container_width=True)
        st.write('''
            The export-import discrepancies, calculated based on origin values, are overwhelmingly negative. 
                This suggests that Armenia's reported imports from the EU are consistently lower than the EU's reported exports to Armenia.
                Such discrepancies could stem from various factors, including differences in valuation methods,
                incomplete reporting by either side,
                possible discrepancies in currency conversion rates or trade classifications.
            Some countries, such as Greece, Romania, and Ireland, exhibit smaller discrepancies, with values close to zero or slightly positive.
                However, countries like Poland, Lithuania, and the Netherlands show substantial negative discrepancies, 
                contributing significantly to the overall mismatch.
        ''')

        yearly_discrepancies = comparison_data.groupby('YEAR')['discrepancy_origin'].sum().reset_index()

        # Sort the data by year (if needed)
        yearly_discrepancies = yearly_discrepancies.sort_values(by='YEAR')

        # Create the bar chart
        fig = px.bar(
            yearly_discrepancies,
            x='YEAR',
            y='discrepancy_origin',
            title='Overall Export-Import Discrepancies (Origin) by Year',
            labels={'YEAR': 'Year', 'discrepancy_origin': 'Average Discrepancy (USD)'},
        )

        # Customize the chart layout
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Overall Discrepancy (USD)',
            xaxis_tickangle=0,
            plot_bgcolor='white',
            yaxis=dict(gridcolor='lightgrey'),
            width=600,
            height=400,
        )
        st.plotly_chart(fig, use_container_width=False)
        st.write('''
                The yearly analysis highlights a significant rise in the magnitude of discrepancies after 2022.
                In 2023, the overall discrepancy reached a peak negative value of approximately USD -2.03 billion. 
                This sharp increase may indicate changes in trade policies, data reporting issues, or economic shifts post-2022.
        ''')


    with tab_kazakhstan:
        combined_df_filtered = preprocess_data_kazakhstan(data_kazakhstan)
        visualize_stacked_bar_chart(combined_df_filtered, 'Kazakhstan')

        state_data = {
            "YEAR": [2019, 2020, 2021, 2022, 2023],
            "Import Value State (USD)": [6693384, 6522173, 5963960, 8008872, 10314009]
        }
        state_df = pd.DataFrame(state_data)
        state_df['Import Value State (USD)'] = state_df['Import Value State (USD)'] * 1000
        eurostat_df = data_kazakhstan.copy()
        
        eurostat_df = eurostat_df[~eurostat_df['REPORTER'].str.contains(
            'Euro area|European Union|Union européenne|Zone euro')]
        
        eurostat_df['YEAR'] = eurostat_df['PERIOD'].str.extract(r'(\d{4})').astype(int)
        eurostat_df = eurostat_df.groupby(['YEAR'])['VALUE_IN_EUR'].sum().reset_index()

        eurostat_df['Exchange Rate'] = eurostat_df['YEAR'].map(exchange_rates)
        eurostat_df['Export Value Eurostat (USD)'] = (
            eurostat_df['VALUE_IN_EUR'] * eurostat_df['Exchange Rate']
        ).round(0)

        comparison_df = pd.merge(
            eurostat_df[['YEAR', 'Export Value Eurostat (USD)']],
            state_df,
            on=['YEAR'],
            how='inner'
        )
        # Calculate discrepancies
        comparison_df['Discrepancy (USD)'] = (
            comparison_df['Export Value Eurostat (USD)'] - comparison_df['Import Value State (USD)']
        )
        comparison_df['Percentage Difference (%)'] = (
            (comparison_df['Discrepancy (USD)'] / comparison_df['Import Value State (USD)']) * 100
        ).round(2)

        st.write('''
            ### Kazakhstan Eurostat vs. State Import Data Comparison
            
            The table below compares export data reported by Eurostat and import data reported by Kazakhstan's state statistics for the years 2019 to 2023. 
        ''')


        st.dataframe(comparison_df)
        st.write('''
                Between 2019 and 2021, discrepancies between Eurostat's export values and Kazakhstan's import values were minor, 
                with differences below 10%, indicating consistent reporting. However, discrepancies surged in 2022 (35.66%, 2.8 billion) and 2023 (25.63%, 2.6 billion). This significant growth aligns with the imposition of post-war sanctions on Russia, 
                suggesting Kazakhstan's role as a transit country helping Russia circumvent these restrictions. 
                Increased trade flows and re-routing of goods likely contributed to these discrepancies, alongside differences 
                in reporting standards. Harmonizing methodologies and closely examining post-2021 trade dynamics is essential 
                to fully understand these shifts.
        ''')

    with tab_uzbekistan:
        combined_df_filtered = preprocess_data(data_uzbekistan)
        visualize_stacked_bar_chart(combined_df_filtered, 'Uzbekistan')

        data_uzbekistan['YEAR'] = data_uzbekistan['PERIOD'].str.extract(r'(\d{4})').astype(int)
        grouped_df = data_uzbekistan.groupby(['REPORTER', 'YEAR'])['VALUE_IN_EUR'].sum().reset_index()
        grouped_df['REPORTER'] = grouped_df['REPORTER'].str.split().str[0]

        # Convert Eurostat values from EUR to USD using exchange rates
        grouped_df['exchange_rate'] = grouped_df['YEAR'].map(exchange_rates)
        grouped_df['Export Value, in USD'] = (grouped_df['VALUE_IN_EUR'] * grouped_df['exchange_rate']).round(0)

        # Prepare Uzbekistan state import data
        uzbekistan_state_stats['YEAR'] = uzbekistan_state_stats['Year'].astype(int)
        uzbekistan_state_stats["Import Value"] = uzbekistan_state_stats["Import Value"].astype(float)
        uzbekistan_state_stats["Import Value"] *= 1000  # Convert to USD
        uzbekistan_state_stats.rename(
            columns={'Klassifikator_en': 'REPORTER', "Import Value": "Import Value, in USD"},
            inplace=True
        )

        # Merge Eurostat and Uzbekistan data
        merged_data_reporter = pd.merge(
            grouped_df[['REPORTER', 'YEAR', 'Export Value, in USD']],  # Use converted values
            uzbekistan_state_stats[['REPORTER', 'YEAR', 'Import Value, in USD']],
            on=['REPORTER', 'YEAR'],
            how='inner'
        )

        # Calculate discrepancies
        merged_data_reporter['Discrepancy (USD)'] = (
            merged_data_reporter['Export Value, in USD'] - merged_data_reporter['Import Value, in USD']
        )
        # Calculate and round percentage differences
        merged_data_reporter['Percentage Difference (%)'] = (
            (merged_data_reporter['Discrepancy (USD)'] / merged_data_reporter['Export Value, in USD']) * 100
        ).round(2)

        # Display combined data and explanation
        st.write('''
            ### Combined Eurostat Data and Uzbekistan State Import Data
            The table below shows export values from Eurostat and import values from Uzbekistan's state statistics. 
            Discrepancies and percentage differences are calculated to highlight mismatches. 
            While some countries align closely, others show significant mismatches, indicating differences 
            in data collection or reporting practices.
        ''')
        st.dataframe(merged_data_reporter)

        # Analyze country-level discrepancies
        country_discrepancies = merged_data_reporter.groupby('REPORTER')['Discrepancy (USD)'].sum().reset_index()
        country_discrepancies.sort_values(by='Discrepancy (USD)', ascending=False, inplace=True)

        # Visualize country-level discrepancies
        fig = px.bar(
            country_discrepancies,
            x='REPORTER',
            y='Discrepancy (USD)',
            title='Total Export-Import Discrepancies (USD) by EU Country to Uzbekistan',
            labels={'REPORTER': 'EU Country', 'Discrepancy (USD)': 'Total Discrepancy (USD)'},
            color='Discrepancy (USD)',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(
            xaxis_title='EU Country',
            yaxis_title='Total Discrepancy (USD)',
            xaxis_tickangle=45,
            plot_bgcolor='white',
            yaxis=dict(gridcolor='lightgrey')
        )
        st.plotly_chart(fig, use_container_width=True)

        # Analyze yearly discrepancies
        yearly_discrepancies = merged_data_reporter.groupby('YEAR')['Discrepancy (USD)'].sum().reset_index()

        # Visualize yearly discrepancies
        fig = px.bar(
            yearly_discrepancies,
            x='YEAR',
            y='Discrepancy (USD)',
            title='Overall Export-Import Discrepancies (USD) by Year to Uzbekistan',
            labels={'YEAR': 'Year', 'Discrepancy (USD)': 'Total Discrepancy (USD)'},
        )
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Total Discrepancy (USD)',
            xaxis_tickangle=0,
            plot_bgcolor='white',
            yaxis=dict(gridcolor='lightgrey'),
            width=600,
            height=400,
        )
        st.plotly_chart(fig, use_container_width=False)

        # Highlight extreme outliers
        extreme_threshold = 1000  # Define threshold for extreme percentage differences
        extreme_outliers = merged_data_reporter[merged_data_reporter['Percentage Difference (%)'].abs() > extreme_threshold]

        st.write('''
            ### Outliers: Extreme Percentage Differences
            The table below highlights countries and years where the percentage difference exceeds 1,000%. 
                 These extreme mismatches often point to systemic issues in data reporting or trade practices. 
                 One potential cause is small trade volumes, where minimal exports reported by Eurostat can amplify percentage 
                 discrepancies even with minor absolute differences. Another contributing factor could be transshipment and rerouting, 
                 as goods may be rerouted through these countries to other destinations, leading to overreporting in Uzbekistan’s data. 
                 Additionally, some discrepancies might arise from omitted or misclassified data, where Eurostat excludes certain low-value transactions, 
                 while Uzbekistan aggregates them under imports from specific countries. Currency conversion or timing issues 
                 may further magnify these mismatches due to differences in exchange rate methodologies or reporting timeframes. 
                 Finally, political or economic factors may play a role, as countries like Ireland, Cyprus, and Malta are often hubs 
                 for financial or trade activities, which may obscure the true origin of goods. These outliers highlight the need 
                 for a more harmonized data collection process and closer inspection of specific trade flows.
        ''')
        st.dataframe(extreme_outliers)


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
