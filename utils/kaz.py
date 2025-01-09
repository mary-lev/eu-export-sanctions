import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List
import logging
import glob
import re

class KazakhstanDataConverter:
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
            # Special groupings and regions
            "Всего": "World",
            "Страны СНГ": "Commonwealth of Independent States",
            "Страны ЕАЭС": "Eurasian Economic Union",
            "Страны ЕС": "European Union - 27 countries (from 2020)",
            "Остальные страны мира": "Rest of the world",
            "Страны вне ЕАЭС": "Non-EAEU countries",
            "Страны вне ЕС": "Non-EU countries",
            
            # EU Countries
            "Австрия": "Austria",
            "Бельгия": "Belgium",
            "Болгария": "Bulgaria",
            "Кипр": "Cyprus",
            "Чешская Республика": "Czechia",
            "Германия": "Germany",
            "Дания": "Denmark",
            "Эстония": "Estonia",
            "Испания": "Spain",
            "Финляндия": "Finland",
            "Франция": "France",
            "Греция": "Greece",
            "Хорватия": "Croatia",
            "Венгрия": "Hungary",
            "Ирландия": "Ireland",
            "Италия": "Italy",
            "Литва": "Lithuania",
            "Люксембург": "Luxembourg",
            "Республика Латвия": "Latvia",
            "Мальта": "Malta",
            "Нидерланды": "Netherlands",
            "Польша": "Poland",
            "Португалия": "Portugal",
            "Румыния": "Romania",
            "Швеция": "Sweden",
            "Словения": "Slovenia",
            "Словакия": "Slovakia",
            
            # CIS and EAEU Countries
            "Армения": "Armenia",
            "Беларусь": "Belarus",
            "Кыргызстан": "Kyrgyzstan",
            "Россия": "Russia",
            "Азербайджан": "Azerbaijan",
            "Молдова, Республика": "Moldova",
            "Таджикистан": "Tajikistan",
            "Туркменистан": "Turkmenistan",
            "Украина": "Ukraine",
            "Узбекистан": "Uzbekistan",
            
            # Other European Countries
            "Соединенное Королевство": "United Kingdom",
            "Швейцария": "Switzerland",
            "Норвегия": "Norway",
            "Исландия": "Iceland",
            "Сербия": "Serbia",
            "Черногория (Монтенегро)": "Montenegro",
            "Македония": "North Macedonia",
            "Албания": "Albania",
            "Босния и Герцеговина": "Bosnia and Herzegovina",
            "Лихтенштейн": "Liechtenstein",
            
            # Asian Countries
            "Китай": "China",
            "Япония": "Japan",
            "Республика Корея": "South Korea",
            "Турция": "Turkey",
            "Индия": "India",
            "Вьетнам": "Vietnam",
            "Индонезия": "Indonesia",
            "Малайзия": "Malaysia",
            "Сингапур": "Singapore",
            "Таиланд": "Thailand",
            "Объединенные Арабские Эмираты": "United Arab Emirates",
            "Саудовская Аравия": "Saudi Arabia",
            "Израиль": "Israel",
            "Иран, Исламская Республика": "Iran",
            "Пакистан": "Pakistan",
            "Бангладеш": "Bangladesh",
            "Монголия": "Mongolia",
            "Тайвань (Китай)": "Taiwan",
            "Гонконг": "Hong Kong",
            
            # Americas
            "Соединенные Штаты Америки": "United States",
            "Канада": "Canada",
            "Мексика": "Mexico",
            "Бразилия": "Brazil",
            "Аргентина": "Argentina",
            "Чили": "Chile",
            "Колумбия": "Colombia",
            "Перу": "Peru",
            
            # Oceania
            "Австралия": "Australia",
            "Новая Зеландия": "New Zealand",
            
            # Africa
            "Египет": "Egypt",
            "Южная Африка": "South Africa",
            "Марокко": "Morocco",
            "Алжир": "Algeria",
            "Нигерия": "Nigeria"
        }

    def extract_year_from_filename(self, filename: str) -> int:
        """Extract year from filename"""
        match = re.search(r'(\d{4})', filename)
        if match:
            return int(match.group(1))
        return None

    def read_kazakhstan_file(self, file_path: str, year: int) -> pd.DataFrame:
        """Read and process a single Kazakhstan Excel file"""
        try:
            print(f"\nProcessing file for year {year}")
            
            # For 2023 file, we need to select the correct sheet
            if year == 2023:
                # Get list of sheets
                excel_file = pd.ExcelFile(file_path)
                sheets = excel_file.sheet_names
                print(f"Available sheets: {sheets}")
                
                # Try to find sheet with '2023' in the name
                target_sheet = None
                for sheet in sheets:
                    if '2023' in str(sheet):
                        target_sheet = sheet
                        break
                
                if target_sheet is None:
                    # If no sheet with '2023', try to find one matching a common pattern
                    for sheet in sheets:
                        if any(keyword in str(sheet).lower() for keyword in ['данные', 'data', 'list']):
                            target_sheet = sheet
                            break
                
                if target_sheet:
                    print(f"Using sheet: {target_sheet}")
                    df = pd.read_excel(file_path, sheet_name=target_sheet, header=None)
                else:
                    # If no suitable sheet found, use first sheet
                    df = pd.read_excel(file_path, sheet_name=0, header=None)
            else:
                # For other years, read the default sheet
                df = pd.read_excel(file_path, header=None)
                
            print(f"Initial shape: {df.shape}")
            print("df", year, df.columns)
            print(f"\nProcessing file for year {year}")
            print(f"Initial shape: {df.shape}")
            
            # Find the start of data
            start_row = None
            for idx, row in df.iterrows():
                if isinstance(row[0], str) and "Всего" in row[0]:
                    start_row = idx
                    break
            
            if start_row is None:
                raise ValueError(f"Could not find data start in file {file_path}")
            
            # Extract data portion
            df_cleaned = df.iloc[start_row:].copy()
            
            # Keep only country and import value columns
            df_cleaned = df_cleaned.iloc[:, [0, 5]]
            df_cleaned.columns = ['country', 'import_value']
            
            # Clean country names and values
            df_cleaned['country'] = df_cleaned['country'].astype(str).str.strip()
            df_cleaned['import_value'] = pd.to_numeric(
                df_cleaned['import_value'].replace(['-', '', ' '], np.nan),
                errors='coerce'
            )
            
            # Add year column
            df_cleaned['year'] = year
            
            # Remove rows with NaN values
            df_cleaned = df_cleaned.dropna()
            
            print(f"Processed shape: {df_cleaned.shape}")
            print("Sample of processed data:")
            print(df_cleaned.head())
            
            return df_cleaned
            
        except Exception as e:
            self.logger.error(f"Error reading file {file_path}: {e}")
            raise

    def process_all_files(self, directory: str) -> pd.DataFrame:
        """Process all Excel files in directory"""
        all_data = []
        
        # Find all Excel files
        file_pattern = Path(directory) / "*.xls*"
        files = glob.glob(str(file_pattern))
        
        for file_path in files:
            try:
                year = self.extract_year_from_filename(file_path)
                print("Year", year)
                if year and 2019 <= year <= 2023:
                    df = self.read_kazakhstan_file(file_path, year)
                    all_data.append(df)
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                continue
        
        if not all_data:
            raise ValueError("No data was successfully processed")
            
        return pd.concat(all_data, ignore_index=True)

    def convert_to_eurostat_format(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convert Kazakhstan data to Eurostat format"""
        try:
            eurostat_data = []
            unmapped_countries = set()
            
            # Regions to exclude (Russian names)
            regions_to_exclude = {
                'Азия', 'Америка', 'Африка', 'Европа', 
                'Австралия и Океания', 'Французские Южные Территории'
            }
            
            for _, row in df.iterrows():
                country = str(row['country']).strip()
                year = int(row['year'])
                import_value = row['import_value']
                
                if pd.isna(import_value) or country.lower() == 'nan':
                    continue
                    
                # Skip Russian region names
                if country in regions_to_exclude:
                    continue
                
                # Convert thousand USD to EUR (multiply by 1000 for full value)
                value_eur = float(import_value * 1000) / self.exchange_rates.get(year, 1.0)
                
                # Map partner names
                partner = self.country_mapping.get(country, country)
                
                # Only include if we have a mapping or if it's already in English
                if country not in self.country_mapping:
                    # Check if the country name uses Cyrillic characters
                    if any(ord(c) >= 1040 and ord(c) <= 1103 for c in country):
                        unmapped_countries.add(country)
                        continue
                
                eurostat_data.append({
                    'REPORTER': 'Kazakhstan',
                    'PARTNER': partner,
                    'PRODUCT': 'TOTAL',
                    'FLOW': 'IMPORT',
                    'STAT_PROCEDURE': 'NORMAL',
                    'PERIOD': f'Y{year}',
                    'VALUE_IN_EUR': round(value_eur, 2)
                })
            
            # if unmapped_countries:
            #     print("\nWarning: Found countries without explicit mapping:")
            #     print(sorted(unmapped_countries))
            
            eurostat_df = pd.DataFrame(eurostat_data)
            
            if not eurostat_df.empty:
                eurostat_df = eurostat_df.sort_values(['PERIOD', 'PARTNER'])
            
            return eurostat_df
            
        except Exception as e:
            self.logger.error(f"Error converting to Eurostat format: {e}")
            raise

    def print_data_summary(self, df: pd.DataFrame):
        """Print summary of the data"""
        if df.empty:
            print("No data to summarize")
            return
            
        print("\nUnique partners in the data:")
        partners = sorted(df['PARTNER'].unique())
        for partner in partners:
            total_value = df[df['PARTNER'] == partner]['VALUE_IN_EUR'].sum()
            # print(f"- {partner}: {total_value:,.2f} EUR total")
            
        print("\nYears covered:")
        for period in sorted(df['PERIOD'].unique()):
            year_total = df[df['PERIOD'] == period]['VALUE_IN_EUR'].sum()
            print(f"- {period}: {year_total:,.2f} EUR total")
            
        print("\nValue ranges:")
        print(f"Min value: {df['VALUE_IN_EUR'].min():,.2f} EUR")
        print(f"Max value: {df['VALUE_IN_EUR'].max():,.2f} EUR")
        print(f"Mean value: {df['VALUE_IN_EUR'].mean():,.2f} EUR")
        
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
    converter = KazakhstanDataConverter()
    
    input_dir = "data/kazakhstan_data"
    output_file = "data/national_data_converted/kazakhstan_import_yearly.csv"
    
    print("Processing Kazakhstan data files...")
    raw_data = converter.process_all_files(input_dir)
    
    print("\nConverting to Eurostat format...")
    eurostat_format_df = converter.convert_to_eurostat_format(raw_data)
    
    if not eurostat_format_df.empty:
        converter.print_data_summary(eurostat_format_df)
        converter.save_output(eurostat_format_df, output_file)
        print(f"\nSuccessfully converted data and saved to {output_file}")
    else:
        print("Error: No data was converted")

if __name__ == "__main__":
    main()