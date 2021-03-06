from tradingview_ta import TA_Handler, Interval, Exchange
from collections import Counter
import sys
import get_exchange_prices


EC2_mode = True if len(sys.argv) == 1 else False

COIN_LIST_PATH = '/home/ec2-user/script/coin_list.txt' if EC2_mode else 'coin_list.txt'
PRICE_ALERT_PERCENTAGE = .08 if EC2_mode else float(sys.argv[1]) / 100

coins, alerted_coins = [], []

with open(COIN_LIST_PATH) as c:
	coins = c.read().splitlines()

coinmarketcap_prices = get_exchange_prices.get_prices_coinmarketcap()
kraken_prices = get_exchange_prices.get_kraken_prices(coins)
#coinbasepro_prices = get_exchange_prices.get_coinbasepro_prices(coins)
binanceUS_prices = get_exchange_prices.get_binanceUS_prices(coins)
kucoin_prices = get_exchange_prices.get_kucoin_prices(coins)
gemini_prices = get_exchange_prices.get_gemini_prices(coins)
bittrex_prices = get_exchange_prices.get_bittrex_prices(coins)

coin_prices = {}
for coin in coins:
	if coin not in coinmarketcap_prices.keys():
		continue
	if coin in kraken_prices:
		coin_prices[(coin,"KRAKEN")] = kraken_prices[coin]
	#if coin in coinbasepro_prices:
		#coin_prices[(coin,"COINBASEPRO")] = coinbasepro_prices[coin]
	if coin in binanceUS_prices:
		coin_prices[(coin,"BINANCEUS")] = binanceUS_prices[coin]
	if coin in kucoin_prices:
		coin_prices[(coin,"KUCOIN")] = kucoin_prices[coin]
	if coin in gemini_prices:
		coin_prices[(coin,"GEMENI")] = gemini_prices[coin]
	if coin in bittrex_prices:
		coin_prices[(coin,"BITTREX")] = bittrex_prices[coin]
	

for c,v in coin_prices.items():
	coin,exchange = c[0],c[1]

	percent_difference = (coinmarketcap_prices[coin] - v) / coinmarketcap_prices[coin] if coinmarketcap_prices[coin] >= v else (coinmarketcap_prices[coin] - v) / v

	if abs(percent_difference) > PRICE_ALERT_PERCENTAGE:
		alerted_coins.append([coin,exchange,round(-100*percent_difference,2),
			"CoinMarketCap_price: {}".format(round(coinmarketcap_prices[coin],3)),
				"{}_price: {}".format(exchange,round(v,3))])


alerted_coins.sort(key=lambda x: abs(x[2]), reverse=True)
for a in alerted_coins:
	a[2] = str(a[2]) + '%'
if len(alerted_coins) > 0:
	print(alerted_coins)
else:
	print([0,0,0,0])
