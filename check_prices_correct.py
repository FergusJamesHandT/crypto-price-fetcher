import pandas as pd
from datetime import datetime


def convert_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).strftime("%Y-%m-%d")


def extract_unique_currencies(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Group by currency and get the first occurrence of each
    unique_currencies = df.groupby("currency").first().reset_index()

    # Select only the relevant columns
    result = unique_currencies[["currency", "timestamp", "usd_price"]]

    # Convert timestamp to YYYY-MM-DD format
    result["date"] = result["timestamp"].apply(convert_timestamp)

    # Sort by currency name
    result = result.sort_values("currency")

    # Reorder columns and drop the original timestamp
    result = result[["currency", "date", "usd_price"]]

    # Save the result to a new CSV file
    result.to_csv(output_file, index=False)

    print(f"Unique currencies extracted. Output saved to {output_file}")


if __name__ == "__main__":
    input_file = "veda-fy24-dws_with_prices_and_year_month.csv"
    output_file = "unique_currencies_sample.csv"
    extract_unique_currencies(input_file, output_file)
