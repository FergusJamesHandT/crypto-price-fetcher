import pandas as pd
from datetime import datetime


def add_year_month_column(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Convert timestamp to datetime and create year-month column
    df["year-month"] = pd.to_datetime(df["timestamp"], unit="ms").dt.strftime("%b-%y")

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Processing complete. Output saved to {output_file}")


if __name__ == "__main__":
    input_file = "veda-fy24-dws_with_prices_updated.csv"
    output_file = "veda-fy24-dws_with_prices_and_year_month.csv"
    add_year_month_column(input_file, output_file)
