from database.database import DatabaseUtils


def main():
    db_utils = DatabaseUtils()
    success = db_utils.get_coingecko_coin_list("coingecko_coin_list.csv")

    if success:
        print("CoinGecko coin list successfully fetched and saved.")
    else:
        print("Failed to fetch or save the CoinGecko coin list.")


if __name__ == "__main__":
    main()
