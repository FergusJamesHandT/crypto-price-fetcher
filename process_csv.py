import pandas as pd
from pricing.pricing import Coingecko
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm

# Set the rate limit for Pro plan
CALLS = 500
RATE_LIMIT = 60  # 60 seconds


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def rate_limited_get_price(cg, currency, timestamp):
    return cg.get_historic_price_at_date(currency, timestamp)


def process_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Initialize Coingecko
    cg = Coingecko()

    # Function to get price for a row
    def get_price(row):
        if pd.notna(row["usd_price"]):
            return row["usd_price"]
        try:
            price_data = rate_limited_get_price(cg, row["currency"], row["timestamp"])
            return price_data["price"] if price_data else None
        except Exception as e:
            print(f"Error processing row: {row}")
            print(f"Error: {e}")
            return None

    # Apply the get_price function to each row with a progress bar
    tqdm.pandas(desc="Processing rows")
    df["usd_price"] = df.progress_apply(get_price, axis=1)

    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

    print(f"Processing complete. Output saved to {output_file}")

    # Print rows with missing usd_price
    missing_prices = df[df["usd_price"].isna()]
    if not missing_prices.empty:
        print("\nRows with missing USD prices:")
        print(missing_prices.to_string())
    else:
        print("\nAll rows have USD prices.")


if __name__ == "__main__":
    input_file = "veda-fy24-dws_with_prices.csv"
    output_file = "veda-fy24-dws_with_prices_updated.csv"
    process_csv(input_file, output_file)
