import csv
import os

import pandas as pd


def clean_and_save_file(input_filename):
    # Read the CSV with specific quote handling
    df = pd.read_csv(input_filename, encoding="cp1252", header=1, quoting=csv.QUOTE_ALL)

    # Set the first unnamed column as index
    df.set_index(df.columns[0], inplace=True)
    df.index.name = "SKU"

    # Remove quotes from all string values
    df.index = df.index.str.replace('"', "")
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].str.replace('"', "")

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

    # Split SKUs and keep only the part before the description
    df.index = pd.Index([x.split(" (")[0] for x in df.index])

    # Create new filename
    base_name = os.path.splitext(input_filename)[0]
    new_filename = f"{base_name}_cleaned.csv"

    # Save to CSV with specific parameters to avoid quotes
    df.to_csv(new_filename, quoting=csv.QUOTE_NONE, escapechar="\\", encoding="utf-8")

    # Print verification
    print("\nVerifying SKU splitting:")
    print(
        "\nFirst few SKUs in cleaned file (should only show part before parentheses):"
    )
    print(df.index.tolist()[:10])


# Use the function
clean_and_save_file("items_sales.CSV")
