import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import logging

class UzbekDataConverter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        self.exchange_rates = {
            2019: 1.12,
            2020: 1.14,
            2021: 1.18,
            2022: 1.05,
            2023: 1.07
        }

        # Mapping for country names to match Eurostat format
        self.country_mapping = {
            # Special groupings
            "European Union": "European Union - 27 countries (from 2020)",
            "EU countries": "European Union - 27 countries (from 2020)",
            "Total": "World",
            "CIS countries": "Commonwealth of Independent States",
            "EAEU countries": "Eurasian Economic Union",
            
            # Individual countries
            "Russian Federation": "Russia",
            "USA": "United States",
            "United Kingdom of Great Britain": "United Kingdom",
            "Great Britain": "United Kingdom",
            "UAE": "United Arab Emirates",
            "Korea, Republic": "South Korea",
            "Czech Republic": "Czechia",
            "Slovak Republic": "Slovakia",
            "Turkiye": "Turkey"
        }

    def read_uzbek_data(self, file_path: str) -> pd.DataFrame:
        """Read and initially process Uzbekistan CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            print("Initial dataframe shape:", df.shape)
            
            # Keep only relevant columns
            df_cleaned = df[['Klassifikator_en'] + [str(year) for year in range(2010, 2024)]]
            
            # Remove rows with missing country names
            df_cleaned = df_cleaned[df_cleaned['Klassifikator_en'].notna()]
            
            # Convert numeric columns to float, replacing '-' with NaN
            year_columns = [str(year) for year in range(2010, 2024)]
            for col in year_columns:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col].replace(['-', ''], np.nan), errors='coerce')
            
            print("Processed dataframe shape:", df_cleaned.shape)
            print("\nUnique English country names found:")
            print(sorted(df_cleaned['Klassifikator_en'].unique()))
            
            return df_cleaned
            
        except Exception as e:
            self.logger.error(f"Error reading Uzbek data: {e}")
            raise

    def convert_to_eurostat_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert Uzbek data to Eurostat format with yearly periods"""
        try:
            eurostat_data = []
            
            # Define EU-27 countries
            eu27_countries = {
                "Austria", "Belgium", "Bulgaria", "Croatia", "Cyprus", 
                "Czechia", "Czech Republic", "Denmark", "Estonia", "Finland",
                "France", "Germany", "Greece", "Hungary", "Ireland", "Italy",
                "Latvia", "Lithuania", "Luxembourg", "Malta", "Netherlands",
                "Poland", "Portugal", "Romania", "Slovakia", "Slovak Republic", 
                "Slovenia", "Spain", "Sweden"
            }
            
            # Dictionary to store EU-27 totals by year
            eu27_totals = {}
            
            # Process only recent years
            recent_years = [str(year) for year in range(2019, 2024)]
            
            # Track any unmapped countries
            unmapped_countries = set()
            
            for year in recent_years:
                year_int = int(year)
                
                for _, row in df.iterrows():
                    country_en = str(row['Klassifikator_en']).strip()
                    yearly_value_usd = row[year]
                    
                    if pd.isna(yearly_value_usd):
                        continue
                    
                    # Convert thousand USD to EUR
                    yearly_value_eur = float(yearly_value_usd * 1000) / self.exchange_rates.get(year_int, 1.0)
                    
                    # Accumulate EU-27 totals
                    if country_en in eu27_countries:
                        eu27_totals[year_int] = eu27_totals.get(year_int, 0) + yearly_value_eur
                    
                    # Map partner names to match Eurostat
                    partner = self.country_mapping.get(country_en, country_en)
                    
                    if country_en not in self.country_mapping and country_en not in eu27_countries:
                        unmapped_countries.add(country_en)
                    
                    # Create yearly record
                    eurostat_data.append({
                        'REPORTER': 'Uzbekistan',
                        'PARTNER': partner,
                        'PRODUCT': 'TOTAL',
                        'FLOW': 'IMPORT',
                        'STAT_PROCEDURE': 'NORMAL',
                        'PERIOD': f'Y{year}',
                        'VALUE_IN_EUR': round(yearly_value_eur, 2)
                    })
            
            # Add EU-27 total rows
            for year, total in eu27_totals.items():
                eurostat_data.append({
                    'REPORTER': 'Uzbekistan',
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
            
            # Convert to DataFrame
            eurostat_df = pd.DataFrame(eurostat_data)
            
            # Sort by period and partner
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
            # Get total value for this partner
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
                
            # Create output directory if it doesn't exist
            Path(output_file).parent.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            df.to_csv(output_file, index=False)
            self.logger.info(f"Saved file: {output_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving file: {e}")
            raise

def main():
    # Initialize converter
    converter = UzbekDataConverter()
    
    # Process data
    input_file = "data/uzbekistan_data/sdmx_data_1176.csv"
    output_file = "data/national_data_converted/uzbek_import_yearly.csv"
    
    print("Reading Uzbek data...")
    uzbek_df = converter.read_uzbek_data(input_file)
    
    print("\nConverting to Eurostat format...")
    eurostat_format_df = converter.convert_to_eurostat_format(uzbek_df)
    
    if not eurostat_format_df.empty:
        converter.print_data_summary(eurostat_format_df)
        converter.save_output(eurostat_format_df, output_file)
        print(f"\nSuccessfully converted data and saved to {output_file}")
    else:
        print("Error: No data was converted")

if __name__ == "__main__":
    main()