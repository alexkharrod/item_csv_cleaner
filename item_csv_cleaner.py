#!/usr/bin/env python3
import csv
import os
import sys
import time

import pandas as pd


def clean_and_save_file(input_filename, output_folder):
    print(f"Attempting to process file: {input_filename}")
    try:
        # Skip if this is already a cleaned file
        if "cleaned" in input_filename:
            print("Skipping already cleaned file")
            return

        # Read the CSV with specific quote handling
        df = pd.read_csv(
            input_filename, encoding="cp1252", header=1, quoting=csv.QUOTE_ALL
        )
        print("File read successfully")

        # Set the first unnamed column as index
        df.set_index(df.columns[0], inplace=True)
        df.index.name = "SKU"
        print("Set index successfully")

        # Remove quotes from all string values
        df.index = df.index.str.replace('"', "")
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = df[col].str.replace('"', "")
        print("Removed quotes successfully")

        # Create mask for categories and totals
        category_mask = (
            (df.index == "Uncategorized")
            | (df.index == "Inventory")
            | (df.index == "Total Inventory")
            | (df.index == "Total Uncategorized")
            | (df.index == "TOTAL")
        )

        # Create mask for SKUs starting with specific numbers
        number_mask = df.index.str.match(r"^(14|16|20|21|70)-")

        # Create mask for BSBI and Seneca
        prefix_mask = (
            df.index.str.startswith("BSBI-")
            | df.index.str.startswith("Seneca-")
            | df.index.str.startswith("BF")
        )

        # Combine all masks and filter
        df = df[~(category_mask | number_mask | prefix_mask)]
        print("Applied all filters successfully")

        # Split SKUs and keep only the part before the description
        df.index = pd.Index([x.split(" (")[0] for x in df.index])

        # Create new filename in output folder
        input_basename = os.path.basename(input_filename)
        base_name = os.path.splitext(input_basename)[0]
        new_filename = os.path.join(output_folder, f"{base_name}_cleaned.csv")
        print(f"Saving to: {new_filename}")

        # Create output directory if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Save to CSV with specific parameters to avoid quotes
        df.to_csv(
            new_filename, quoting=csv.QUOTE_NONE, escapechar="\\", encoding="utf-8"
        )
        print("File saved successfully to output folder")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    print("Main block starting...")
    # Check if we have enough arguments
    if len(sys.argv) < 3:
        print("Usage: python3 item_csv_cleaner.py input_file output_folder")
        sys.exit(1)

    input_file = sys.argv[1]
    output_folder = sys.argv[2]

    print(f"Processing file: {input_file}")
    print(f"Output folder: {output_folder}")
    clean_and_save_file(input_file, output_folder)
    print("Script completed successfully")
