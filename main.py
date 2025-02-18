import pandas as pd
import os
import csv

def clean_and_save_file(input_filename):
    # Read the CSV with specific quote handling
    df = pd.read_csv(input_filename, 
                     encoding='cp1252',
                     header=1,
                     quoting=csv.QUOTE_ALL)  # Handle all quotes
    
    # Set the first unnamed column as index
    df.set_index(df.columns[0], inplace=True)
    df.index.name = 'SKU'
    
    # Remove quotes from all string values
    df.index = df.index.str.replace('"', '')
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col] = df[col].str.replace('"', '')
    
    # Create mask for categories and totals
    category_mask = (
        (df.index == "Uncategorized") |
        (df.index == "Inventory") |
        (df.index == "Total Inventory") |
        (df.index == "Total Uncategorized") |
        (df.index == "TOTAL")
    )
    
    # Create mask for SKUs starting with specific numbers
    sku_mask = df.index.str.match(r'^(14|16|20|21|70)-')
    
    # Combine masks and filter
    df = df[~(category_mask | sku_mask)]
    
    # Create new filename
    base_name = os.path.splitext(input_filename)[0]
    new_filename = f"{base_name}_cleaned.csv"
    
    # Save to CSV with specific parameters to avoid quotes
    df.to_csv(new_filename, 
              quoting=csv.QUOTE_NONE,  # Don't add any quotes
              escapechar='\\',         # Use backslash as escape character
              encoding='utf-8')        # Use UTF-8 encoding
    
    # Print verification
    print("\nVerifying no quotes remain in SKUs:")
    with open(new_filename, 'r', encoding='utf-8') as f:
        first_lines = [next(f) for _ in range(10)]
        print("First few lines of output file:")
        for line in first_lines:
            print(line.strip())

# Use the function
clean_and_save_file('items_sales.CSV')