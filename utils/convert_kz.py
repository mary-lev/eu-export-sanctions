import pandas as pd
import glob
from pathlib import Path

def convert_period_format(period: str) -> str:
    """Convert period from '202408-Aug. 2024' to 'Aug. 2024' format"""
    try:
        # Split on the hyphen and take the second part
        return period.split('-')[1]
    except:
        return period

def process_file(file_path: str, output_path: str):
    """Process a single file and save with converted dates"""
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Convert PERIOD column
        df['PERIOD'] = df['PERIOD'].apply(convert_period_format)
        
        # Save processed file
        print(f"Saving to: {output_path}")
        df.to_csv(output_path, index=False)
        print(f"Processed: {file_path}")
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def main():
    # Input and output directories
    input_dir = "data/kazahstan_export_eurostat"
    output_dir = "data/kazakhstan_export_eurostat_converted"
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Process all CSV files in the input directory
    for file_path in glob.glob(f"{input_dir}/*.csv"):
        # Create output path
        file_name = Path(file_path).name
        output_path = str(Path(output_dir) / file_name)
        
        # Process file
        process_file(file_path, output_path)

if __name__ == "__main__":
    main()