from pricing import Coingecko

cg = Coingecko()
test_symbols = [("BTC"), ("ETH"), ("FAKE_SYMBOL")]
test_dates = ["2023-10-24 14:00:00", "20-10-24 14:00:00"]
test_data = [
    {"coin_id": "bitcoin", "date": "20-1-2021"},
    {"coin_id": "bollockscoin", "date": "20-21-2021"},
    {"coin_id": "btc", "date": "23-10-24"},
]
final_test_data = [
    {"coin_symbol": "BTC", "date": "2023-10-24 14:00:00"},
    {"coin_symbol": "BOLLOCKSCOIN", "date": "2023-10-24 14:00:00"},
    {"coin_symbol": "BTC", "date": "20-10-24 14:00:00"},
]
# // TEST FOR get_coin_id_by_symbol // #

# for coin_symbol in test_symbols:
#     print(f"Testing with coin Symbol: {coin_symbol}")
#     coin_id = cg.get_cg_id(coin_symbol)
#     if coin_id is not None:
#         print(f"the id of {coin_symbol} is {coin_id}")
#     else:
#         print("Failed to fetch coin id from symbol")

# // TEST FOR format_data_past // #

# for time in test_dates:

#     formatted_time = cg.format_date_past(time)
#     print(formatted_time)


# # // TEST FOR get_historic_price // #

# for coin in test_data:
#     print(f"Testing with coin ID: {coin}")
#     price_data = cg.get_historic_price(coin["coin_id"], coin["date"])
#     if price_data is not None:
#         print(price_data)
#     else:
#         print("Failed to fetch the price.")
#     print()

# // TEST FOR get_price_by_symbol // #

for coin in final_test_data:

    coin_symbol = coin["coin_symbol"]
    print(f"Testing with coin Symbol: {coin_symbol}")
    print(coin["date"])
    print(coin["coin_symbol"])
    price_data = cg.get_price_by_symbol(coin["coin_symbol"], coin["date"])
    if price_data is not None:
        print(f"the price data of {coin_symbol} is {price_data}")
    else:
        print("Failed to fetch coin id from symbol")
