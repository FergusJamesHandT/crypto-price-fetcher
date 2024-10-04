import os
from dotenv import load_dotenv
import psycopg2
import requests
import pandas as pd


class DatabaseUtils:
    """
    Class containing functionality related to maintaining the PostgreSQL database.

    **Attributes:**
        None

    **Methods:**
        **connect_to_db:** Establishes a connection to the PostgreSQL database.
        **check_if_coin_in_db:** Checks if a coin exists in the database.
        **get_coingecko_coin_list:** Fetches the CoinGecko coin list and saves it to a CSV file.
    """

    class DatabaseError(Exception):
        """Custom exception for database errors."""

        def __init__(self, function_name, message="Database error occurred", data=None):
            self.function_name = function_name
            self.dev_message = f"Error in {function_name}: {message}"
            self.client_message = message
            self.data = data
            super().__init__(self.client_message)

    def __init__(self) -> None:
        pass

    def connect_to_db(self):
        """
        Establishes a connection to the PostgreSQL database.

        **Args:**
            None

        **Returns:**
            psycopg2.extensions.connection: A connection object representing the connection to the database.
        """

        load_dotenv()
        username = os.getenv(key="AZ_PSQL_USERNAME")
        password = os.getenv(key="AZ_PSQL_PASSWORD")
        host = os.getenv(key="AZ_PSQL_HOST")
        port = os.getenv(key="AZ_PSQL_PORT")
        dbname = os.getenv(key="AZ_PSQL_DATABASE_NAME")

        cnxn = psycopg2.connect(
            dsn=f"user={username} password={password} host={host} port={port} dbname={dbname} sslmode=require"
        )

        return cnxn

    def check_if_coin_in_db(self, symbol: str):
        """
        Checks if a coin exists in the database.

        **Args:**
            symbol (str): The symbol of the coin to check.

        **Returns:**
            list: A list of tuples containing information about the coin if found, or an empty list if not found.
        """
        conn = None
        try:
            conn = self.connect_to_db()

            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                            SELECT * FROM assets
                            WHERE symbol = %s
                        """,
                        (symbol,),
                    )

                    coin_info = cursor.fetchall()

                    return coin_info

        except Exception as error:
            print(f"Check coin exists error: {error}")

        finally:
            if conn is not None:
                cursor.close()
                conn.close()

    def get_coingecko_coin_list(self, output_file="coingecko_coin_list.csv"):
        """
        Fetches the CoinGecko coin list and saves it to a CSV file.

        Args:
            output_file (str): The name of the output CSV file. Defaults to 'coingecko_coin_list.csv'.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            # CoinGecko API endpoint for coin list
            url = "https://api.coingecko.com/api/v3/coins/list"

            # Make the API request
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses

            # Convert the JSON response to a DataFrame
            coin_list = pd.DataFrame(response.json())

            # Save the DataFrame to a CSV file
            coin_list.to_csv(output_file, index=False)

            print(f"CoinGecko coin list saved to {output_file}")
            return True

        except requests.RequestException as e:
            print(f"Error fetching CoinGecko coin list: {e}")
            return False

        except Exception as e:
            print(f"Error saving CoinGecko coin list to CSV: {e}")
            return False
