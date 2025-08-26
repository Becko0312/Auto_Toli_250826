#!/usr/bin/env python3
import json
import re

def expand_abbreviations(text: str) -> str:
    """Expand FR and RR abbreviations in automotive terms"""
    
    # Replace FR with FRONT (word boundary to avoid partial matches)
    text = re.sub(r'\bFR\b', 'FRONT', text)
    
    # Replace RR with REAR (word boundary to avoid partial matches)  
    text = re.sub(r'\bRR\b', 'REAR', text)
    
    return text

def fix_fr_rr_abbreviations(input_file: str, output_file: str):
    """Fix FR/RR abbreviations in the dictionary data"""
    
    print(f"Loading data from {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Processing {len(data)} entries...")
    
    # Count changes made
    changes_made = 0
    
    # Process each entry
    for entry in data:
        # Check English column for FR/RR
        original_english = entry["english"]
        expanded_english = expand_abbreviations(original_english)
        
        if original_english != expanded_english:
            entry["english"] = expanded_english
            changes_made += 1
            print(f"Changed: '{original_english}' → '{expanded_english}'")
        
        # Also check Mongolian column (in case there are any)
        original_mongolian = entry["mongolian"]
        expanded_mongolian = expand_abbreviations(original_mongolian)
        
        if original_mongolian != expanded_mongolian:
            entry["mongolian"] = expanded_mongolian
            changes_made += 1
            print(f"Changed: '{original_mongolian}' → '{expanded_mongolian}'")
    
    print(f"\nTotal changes made: {changes_made}")
    
    # Save updated data
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"Updated data saved to {output_file}")

if __name__ == "__main__":
    fix_fr_rr_abbreviations("dictionary.json", "dictionary_fr_rr_fixed.json")