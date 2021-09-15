from coinbase.wallet.client import Client

client = Client(<a,b)
a = client.get_accounts()
b = client.get_currencies()
c = client.get_exchange_rates(currency="BTC")
ltc_sell = client.get_sell_price(currency_pair="DOGE-XOF")
ltc_buy = client.get_buy_price(currency_pair="DOGE-XOF")
print(ltc_sell)
print(ltc_buy)
