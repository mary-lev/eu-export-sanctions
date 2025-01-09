import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import logging

class ArmeniaDataConverter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.exchange_rates = {
            2019: 1.12,
            2020: 1.14,
            2021: 1.18,
            2022: 1.05,
            2023: 1.07
        }

        self.country_mapping = {
            "EU": "European Union - 27 countries (from 2020)",
            "European Union": "European Union - 27 countries (from 2020)",
            "Total": "World",
            "CIS": "Commonwealth of Independent States",
            "EAEU": "Eurasian Economic Union",
            "Russian Federation": "Russia",
            "USA": "United States",
            "UK": "United Kingdom"
        }

    def read_armenia_data(self, file_path: str) -> pd.DataFrame:
        """Read and initially process Armenia CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            print("Initial dataframe shape:", df.shape)
            
            # Filter for yearly data only
            df_cleaned = df[df['timeperiod'] == 'Year'].copy()
            
            # Convert country column to string and handle NaN values
            df_cleaned['country'] = df_cleaned['country'].fillna('Unknown').astype(str)
            
            # Convert import_consigment to numeric, handling '-' values
            df_cleaned['import_consigment'] = pd.to_numeric(
                df_cleaned['import_consigment'].replace(['-', ''], np.nan), 
                errors='coerce'
            )
            
            # Filter recent years
            df_cleaned = df_cleaned[df_cleaned['year'].between(2019, 2023)]
            
            # Remove rows where country is numeric or empty
            df_cleaned = df_cleaned[
                ~df_cleaned['country'].str.match(r'^\d*\.?\d*$') & 
                (df_cleaned['country'] != 'Unknown')
            ]
            
            print("Processed dataframe shape:", df_cleaned.shape)
            print("\nUnique country names found:")
            unique_countries = sorted([c for c in df_cleaned['country'].unique() if isinstance(c, str)])
            print(unique_countries)
            
            return df_cleaned
            
        except Exception as e:
            self.logger.error(f"Error reading Armenia data: {e}")
            raise

    def convert_to_eurostat_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert Armenia data to Eurostat format with yearly periods"""
        try:
            eurostat_data = []
            unmapped_countries = set()
            
            # Define EU-27 countries
            eu27_countries = {
                "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", 
                "Czechia", "Czech Republic", "Denmark", "Estonia", "Finland",
                "France", "Germany", "Greece", "Hungary", "Ireland", "Italy",
                "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
                "Poland", "Portugal", "Romania", "Slovakia", "Slovenia",
                "Spain", "Sweden"
            }
            
            # Dictionary to store EU-27 totals by year
            eu27_totals = {}
            
            for _, row in df.iterrows():
                country = str(row['country']).strip()
                year = int(row['year'])
                import_value = row['import_consigment']
                
                if pd.isna(import_value):
                    continue
                
                # Convert thousand USD to EUR (multiply by 1000 since values are in thousands)
                value_eur = (float(import_value) * 1000) / self.exchange_rates.get(year, 1.0)
                
                # Accumulate EU-27 totals
                if country in eu27_countries:
                    eu27_totals[year] = eu27_totals.get(year, 0) + value_eur
                
                # Map partner names
                partner = self.country_mapping.get(country, country)
                
                if country not in self.country_mapping and country not in eu27_countries:
                    unmapped_countries.add(country)
                
                eurostat_data.append({
                    'REPORTER': 'Armenia',
                    'PARTNER': partner,
                    'PRODUCT': 'TOTAL',
                    'FLOW': 'IMPORT',
                    'STAT_PROCEDURE': 'NORMAL',
                    'PERIOD': f'Y{year}',
                    'VALUE_IN_EUR': round(value_eur, 2)
                })
            
            # Add EU-27 total rows
            for year, total in eu27_totals.items():
                eurostat_data.append({
                    'REPORTER': 'Armenia',
                    'PARTNER': 'European Union - 27 countries (from 2020)',
                    'PRODUCT': 'TOTAL',
                    'FLOW': 'IMPORT',
                    'STAT_PROCEDURE': 'NORMAL',
                    'PERIOD': f'Y{year}',
                    'VALUE_IN_EUR': round(total, 2)
                })
            
            if unmapped_countries:
                print("\nWarning: Found countries without explicit mapping:")
                print(sorted(unmapped_countries))
                print("These will be used as-is. Please verify if they match Eurostat naming conventions.")
            
            eurostat_df = pd.DataFrame(eurostat_data)
            
            if not eurostat_df.empty:
                eurostat_df = eurostat_df.sort_values(['PERIOD', 'PARTNER'])
            
            return eurostat_df
            
        except Exception as e:
            self.logger.error(f"Error converting to Eurostat format: {e}")
            raise

    def print_data_summary(self, df: pd.DataFrame):
        """Print summary of the data for verification"""
        if df.empty:
            print("No data to summarize")
            return
            
        print("\nUnique partners in the data:")
        partners = sorted(df['PARTNER'].unique())
        for partner in partners:
            total_value = df[df['PARTNER'] == partner]['VALUE_IN_EUR'].sum()
            print(f"- {partner}: {total_value:,.2f} EUR total")
            
        print("\nYears covered:")
        for period in sorted(df['PERIOD'].unique()):
            year_total = df[df['PERIOD'] == period]['VALUE_IN_EUR'].sum()
            print(f"- {period}: {year_total:,.2f} EUR total")
            
        print("\nValue ranges:")
        print(f"Min value: {df['VALUE_IN_EUR'].min():,.2f} EUR")
        print(f"Max value: {df['VALUE_IN_EUR'].max():,.2f} EUR")
        print(f"Mean value: {df['VALUE_IN_EUR'].mean():,.2f} EUR")
        print(f"Total value: {df['VALUE_IN_EUR'].sum():,.2f} EUR")
        
        print("\nSample of values (top 5 by value):")
        pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x))
        print(df.nlargest(5, 'VALUE_IN_EUR'))

    def save_output(self, df: pd.DataFrame, output_file: str):
        """Save data to CSV file in Eurostat format"""
        try:
            if df.empty:
                raise ValueError("No data to save")
                
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(output_file, index=False)
            self.logger.info(f"Saved file: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving file: {e}")
            raise

def main():
    converter = ArmeniaDataConverter()
    
    input_file = "data/armenia_data/armenia_data.csv"
    output_file = "data/national_data_converted/armenia_import_yearly.csv"
    
    print("Reading Armenia data...")
    armenia_df = converter.read_armenia_data(input_file)
    
    print("\nConverting to Eurostat format...")
    eurostat_format_df = converter.convert_to_eurostat_format(armenia_df)
    
    if not eurostat_format_df.empty:
        converter.print_data_summary(eurostat_format_df)
        converter.save_output(eurostat_format_df, output_file)
        print(f"\nSuccessfully converted data and saved to {output_file}")
    else:
        print("Error: No data was converted")

if __name__ == "__main__":
    main()