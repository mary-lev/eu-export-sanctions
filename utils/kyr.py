import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import logging

class KyrgyzDataConverter:
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
            # Special groupings
            "The EU": "European Union - 27 countries (from 2020)",
            "Total": "World",
            "CIS": "Commonwealth of Independent States",
            "SCO": "Shanghai Cooperation Organisation",
            "EAEU": "Eurasian Economic Union",
            
            # Countries that might need standardization
            "Russian Federation": "Russia",
            "USA": "United States",
            "UK": "United Kingdom",
            "UAE": "United Arab Emirates",
            "Great Britain": "United Kingdom",
            "Korea": "South Korea",
            "Czech Republic": "Czechia"
        }

    def read_kyrgyz_data(self, file_path: str) -> pd.DataFrame:
        """Read and initially process Kyrgyzstan Excel file"""
        try:
            # Read Excel file
            df = pd.read_excel(file_path, header=None)
            
            print("Initial dataframe shape:", df.shape)
            
            # Extract the data portion with countries and values
            df_cleaned = df.iloc[2:, :]
            print(df_cleaned.head())
            
            # Get actual column count
            actual_columns = df_cleaned.shape[1]
            
            # Create column names
            col_names = ['Country_KZ', 'Country_RU', 'Country_EN']
            year_start = 1994
            year_end = year_start + (actual_columns - 3)
            col_names.extend([str(year) for year in range(year_start, year_end)])
            
            # Assign column names
            df_cleaned.columns = col_names
            print("Columns", df_cleaned.columns)
            
            # Remove rows with missing country names
            df_cleaned = df_cleaned[df_cleaned['Country_EN'].notna()]
            
            # Convert numeric columns to float, replacing '-' with NaN
            year_columns = [col for col in df_cleaned.columns if col.isdigit()]
            for col in year_columns:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col].replace(['-', ''], np.nan), errors='coerce')
            
            print("Processed dataframe shape:", df_cleaned.shape)
            print("Columns:", df_cleaned.columns.tolist())
            
            return df_cleaned
            
        except Exception as e:
            self.logger.error(f"Error reading Kyrgyz data: {e}")
            raise

    def convert_to_eurostat_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert Kyrgyz data to Eurostat format with yearly periods"""
        try:
            eurostat_data = []
            
            # Process only recent years
            recent_years = [str(year) for year in range(2019, 2024)]
            
            # Track any unmapped countries
            unmapped_countries = set()
            
            for year in recent_years:
                year_int = int(year)
                
                for _, row in df.iterrows():
                    country_en = str(row['Country_EN']).strip()
                    yearly_value_usd = row[year]
                    
                    if pd.isna(yearly_value_usd):
                        continue
                    
                    # Convert thousand USD to EUR
                    yearly_value_eur = float(yearly_value_usd * 1000) / self.exchange_rates.get(year_int, 1.0)
                    
                    # Map partner names to match Eurostat
                    partner = self.country_mapping.get(country_en, country_en)
                    
                    if country_en not in self.country_mapping:
                        unmapped_countries.add(country_en)
                    
                    # Create yearly record
                    eurostat_data.append({
                        'REPORTER': 'Kyrgyzstan',
                        'PARTNER': partner,
                        'PRODUCT': 'TOTAL',
                        'FLOW': 'IMPORT',
                        'STAT_PROCEDURE': 'NORMAL',
                        'PERIOD': f'Y{year}',
                        'VALUE_IN_EUR': round(yearly_value_eur, 2)
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
            
        print("\nYears covered:")
        for period in sorted(df['PERIOD'].unique()):
            print(f"- {period}")
            
        print("\nValue ranges:")
        print(f"Min value: {df['VALUE_IN_EUR'].min():,.2f} EUR")
        print(f"Max value: {df['VALUE_IN_EUR'].max():,.2f} EUR")
        print(f"Mean value: {df['VALUE_IN_EUR'].mean():,.2f} EUR")
        
        print("\nSample of values:")
        pd.set_option('display.float_format', lambda x: '{:,.2f}'.format(x))
        print(df.head())

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
    converter = KyrgyzDataConverter()
    
    # Process data
    input_file = "data/kyrgyzstan_data/4.03.00.20 Географическое распределение импорта товаров..xlsx"
    output_file = "national_data_converted/kyrgyz_import_yearly.csv"
    
    print("Reading Kyrgyz data...")
    kyrgyz_df = converter.read_kyrgyz_data(input_file)
    
    print("\nOriginal data structure:")
    print(kyrgyz_df.head())
    print("\nColumns:", kyrgyz_df.columns.tolist())
    
    print("\nConverting to Eurostat format...")
    eurostat_format_df = converter.convert_to_eurostat_format(kyrgyz_df)
    
    if not eurostat_format_df.empty:
        converter.print_data_summary(eurostat_format_df)
        converter.save_output(eurostat_format_df, output_file)
        print(f"\nSuccessfully converted data and saved to {output_file}")
    else:
        print("Error: No data was converted")

if __name__ == "__main__":
    main()