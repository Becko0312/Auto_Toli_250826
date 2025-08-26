#!/usr/bin/env python3
"""
Excel to JSON converter for Mongolian-English Dictionary
Usage: python excel_to_json.py <excel_file_path>
"""

import pandas as pd
import json
import sys
import os

def convert_excel_to_json(excel_file_path, output_file='dictionary.json'):
    """
    Convert Excel dictionary file to JSON format.
    
    Args:
        excel_file_path (str): Path to the Excel file
        output_file (str): Output JSON file name
    """
    try:
        # Read Excel file
        print(f"Reading Excel file: {excel_file_path}")
        df = pd.read_excel(excel_file_path)
        
        # Get column names
        columns = df.columns.tolist()
        print(f"Found columns: {columns}")
        
        # Assume first column is Mongolian, second is English
        if len(columns) < 2:
            raise ValueError("Excel file must have at least 2 columns")
        
        mongolian_col = columns[0]
        english_col = columns[1]
        
        print(f"Using '{mongolian_col}' as Mongolian column")
        print(f"Using '{english_col}' as English column")
        
        # Convert to dictionary format
        dictionary_data = []
        
        for index, row in df.iterrows():
            mongolian_word = str(row[mongolian_col]).strip()
            english_translation = str(row[english_col]).strip()
            
            # Skip empty rows
            if pd.isna(row[mongolian_col]) or pd.isna(row[english_col]):
                continue
            if mongolian_word == 'nan' or english_translation == 'nan':
                continue
            if not mongolian_word or not english_translation:
                continue
                
            dictionary_data.append({
                'mongolian': mongolian_word,
                'english': english_translation
            })
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(dictionary_data, f, ensure_ascii=False, indent=2)
        
        print(f"\nConversion successful!")
        print(f"Created {output_file} with {len(dictionary_data)} entries")
        print(f"First few entries:")
        for i, entry in enumerate(dictionary_data[:3]):
            print(f"  {i+1}. {entry['mongolian']} → {entry['english']}")
            
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{excel_file_path}' not found")
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python excel_to_json.py <excel_file_path>")
        print("\nExample:")
        print("  python excel_to_json.py mongolian_dictionary.xlsx")
        return
    
    excel_file = sys.argv[1]
    
    if not os.path.exists(excel_file):
        print(f"Error: File '{excel_file}' does not exist")
        return
    
    success = convert_excel_to_json(excel_file)
    
    if success:
        print(f"\nYou can now open index.html in your browser to use the dictionary!")
    else:
        print(f"\nConversion failed. Please check the error messages above.")

if __name__ == "__main__":
    main()