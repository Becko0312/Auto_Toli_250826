#!/usr/bin/env python3
import json
import re
from typing import List, Dict

def clean_oil_specifications(text: str) -> str:
    """Remove oil grade specifications and other technical codes using AI-like pattern recognition"""
    
    # Remove oil grade specifications first (more specific patterns first)
    text = re.sub(r'/GF-\d+[A-Z]*\d*W-?\d*', '', text)  # Remove /GF-6A0W-20
    text = re.sub(r'C\d+W-?\d+', '', text)  # Remove C20W-30 style
    text = re.sub(r'\b\d{1,2}W-?\d{2}\b', '', text)  # Standard oil grades
    text = re.sub(r'ENGINE OILC', 'ENGINE OIL', text)  # Fix concatenation issue
    
    # Remove API oil classifications
    text = re.sub(r'/[A-Z]{2,3}', '', text)  # Remove /CF, /GF etc
    text = re.sub(r'\bSN/CF\b', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\bSP/GF\b', '', text, flags=re.IGNORECASE)
    
    # Remove volume specifications (4L, 20L, etc.)
    text = re.sub(r'\b\d+[lL]\b', '', text)
    
    # Remove bulb wattage specifications (5W, 21W, 55W, etc.) when followed by BULB
    text = re.sub(r'\b\d{1,3}W(?=.*BULB)', '', text)
    
    # Remove technical product codes that look like oil specifications
    text = re.sub(r'\bTGMO[A-Z]*', 'ENGINE OIL', text)
    
    # Clean up extra spaces and punctuation
    text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'^\s+|\s+$', '', text)  # Trim
    text = re.sub(r'\s*-\s*$', '', text)  # Remove trailing dashes
    text = re.sub(r'^\s*-\s*', '', text)  # Remove leading dashes
    
    return text

def clean_entry(entry: Dict[str, str]) -> Dict[str, str]:
    """Clean a single dictionary entry"""
    cleaned_entry = {
        "mongolian": clean_oil_specifications(entry["mongolian"]),
        "english": clean_oil_specifications(entry["english"])
    }
    
    # Additional English-specific cleaning
    english = cleaned_entry["english"]
    
    # Simplify common automotive terms
    english = re.sub(r'\bELEMENTKIT\b', 'ELEMENT', english)
    english = re.sub(r'\bFILTERKIT\b', 'FILTER', english)
    english = re.sub(r'\bPADKIT\b', 'PAD', english)
    english = re.sub(r'\bBULB12V\b', 'BULB', english)
    
    # Clean up extra spaces again
    cleaned_entry["english"] = re.sub(r'\s+', ' ', english).strip()
    
    return cleaned_entry

def is_valid_entry(entry: Dict[str, str]) -> bool:
    """Check if entry is valid after cleaning"""
    mongolian = entry["mongolian"].strip()
    english = entry["english"].strip()
    
    # Skip entries that are too short or empty
    if len(mongolian) < 2 or len(english) < 2:
        return False
    
    # Skip entries that are just numbers or codes
    if mongolian.isdigit() or english.isdigit():
        return False
    
    return True

def remove_duplicates(entries: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove duplicate entries based on cleaned text"""
    seen = set()
    unique_entries = []
    
    for entry in entries:
        # Create a key for duplicate detection (normalize case and spacing)
        key = (
            entry["mongolian"].lower().strip(),
            entry["english"].lower().strip()
        )
        
        if key not in seen:
            seen.add(key)
            unique_entries.append(entry)
    
    return unique_entries

def clean_dictionary_data(input_file: str, output_file: str):
    """Main function to clean the dictionary data"""
    
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Original entries: {len(data)}")
    
    # Clean each entry
    print("Cleaning entries...")
    cleaned_data = []
    for entry in data:
        cleaned_entry = clean_entry(entry)
        if is_valid_entry(cleaned_entry):
            cleaned_data.append(cleaned_entry)
    
    print(f"Valid entries after cleaning: {len(cleaned_data)}")
    
    # Remove duplicates
    print("Removing duplicates...")
    final_data = remove_duplicates(cleaned_data)
    
    print(f"Final unique entries: {len(final_data)}")
    print(f"Removed {len(data) - len(final_data)} entries total")
    
    # Save cleaned data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    clean_dictionary_data("dictionary.json", "dictionary_cleaned.json")