import os
from dotenv import load_dotenv
from database.database import DatabaseUtils
import requests
import pandas as pd
from datetime import datetime
import pytz


load_dotenv()


class Coingecko:
    """
    Class containing functionality related to interacting with the CoinGecko API.

    **Attributes:**
        None

    **Methods:**
        **get_cg_id(symbol):**
            Retrieves the CoinGecko ID for a given cryptocurrency symbol.

        **format_date_past(date_str):**
            Formats a date string from 'YYYY-MM-DD HH:MM:SS' to 'DD-MM-YYYY'.

        **get_historic_price(coin_id, date):**
            Retrieves the historic price of a cryptocurrency based on its CoinGecko ID and date.

        **get_price_by_symbol(coin_symbol, date):**
            Retrieves the price of a cryptocurrency by its symbol and date.

    Note:
        Requires further development later of the get_historic_price function. refer to it's docstring for details
    """

    BASE_URL = "https://pro-api.coingecko.com/api/v3"

    def __init__(self):
        self.api_key = os.getenv("COINGECKO_API_KEY")
        self.dbu = DatabaseUtils()

    def format_date_past(self, end_time):
        """
        Formats a Unix timestamp (in milliseconds) to 'DD-MM-YYYY' format.

        **Args:**
            end_time (int): The Unix timestamp in milliseconds to format.

        **Returns:**
            str: The formatted date string if successful, None otherwise.
        """

        end_time = int(end_time) / 1000  # Convert milliseconds to seconds

        utc_datetime = datetime.fromtimestamp(end_time, tz=pytz.UTC)

        date_string = utc_datetime.strftime("%d-%m-%Y")

        if date_string:
            return date_string
        else:
            print("Invalid date format")
        return None

    def get_cg_id(self, symbol):
        """
        Retrieve the CoinGecko ID of a cryptocurrency symbol.


        Args:
            symbol (str): The symbol of the cryptocurrency.

        Returns:
            str: The CoinGecko ID of the cryptocurrency.
        """

        coin = self.dbu.check_if_coin_in_db(symbol=symbol)
        columns = [
            "asset_id",
            "name",
            "symbol",
            "coingecko_id",
            "token_addresses",
            "trading_venues",
            "fiat",
        ]
        coin_df = pd.DataFrame(coin, columns=columns)

        for _, row in coin_df.iterrows():
            if row["fiat"] == True:
                coin_info = {
                    "symbol": symbol,
                    "fiat": row["fiat"],
                }
                return coin_info
            else:
                coin_info = {
                    "symbol": symbol,
                    "coingecko_id": row["coingecko_id"],
                    "fiat": row["fiat"],
                }
                return coin_info

    def get_historic_price(self, coin_info, date):

        if coin_info["fiat"] == True:

            coin_data = {
                "coin_id": coin_info["symbol"],
                "fiat": coin_info["fiat"],
                "price": 1,
                "date": date,
            }
            return coin_data
        else:
            try:
                url = f"{self.BASE_URL}/coins/{coin_info['coingecko_id']}/history?date={date}&localization=false"
                headers = {
                    "Content-Type": "application/json",
                    "x-cg-pro-api-key": self.api_key,
                }
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    data = response.json()

                    return {
                        "coin_id": data["id"],
                        "fiat": coin_info["fiat"],
                        "price": data["market_data"]["current_price"]["usd"],
                        "date": date,
                    }

            except Exception as err:
                print(f"There was an error (get_historic_price): {err}")

    def get_historic_price_at_date(self, coin_symbol, date):

        print(f"coin symbol being searched: {coin_symbol}")
        formatted_date = self.format_date_past(date)
        coin_info = self.get_cg_id(coin_symbol)
        historic_data = self.get_historic_price(coin_info, formatted_date)
        return historic_data
        # print(historic_data)
