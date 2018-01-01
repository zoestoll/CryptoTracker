from binance.client import Client
import time
from datetime import datetime, timedelta
import argparse


parser = argparse.ArgumentParser(description='Find volume change over time for Binance tickers.')
parser.add_argument('apiKey', type=str,
                    help='your binance api key')
parser.add_argument('apiSecret', type=str,
                    help='your binance api secret')
parser.add_argument('interval', choices=['1m','3m','5m','15m','30m','1h','2h','4h','6h','8h','12h','1d','3d','1w','1M'],
                    help='your binance api secret')

args = parser.parse_args()

client = Client(args.apiKey, args.apiSecret)
tickers = client.get_all_tickers()
endTime = int(time.time() * 1000)
startTime = int(time.mktime((datetime.today() - timedelta(days=1)).timetuple()))*1000

for ticker in tickers:
	
	symbol = ticker['symbol']

	# Only looking at BTC data
	if symbol[len(symbol)-3:len(symbol)] != 'BTC':
		continue
	candles = client.get_klines(symbol=symbol, interval=args.interval, startTime=startTime, endTime=endTime)
	volList = []
	for candle in candles:
		openTime = candle[0]
		volume = candle[7]
		volList.append([openTime,volume])

	# Get differences in volume
	diffList = []
	for i in range(1,len(volList)):
		currData = volList[i]
		currVolume = float(currData[1])
		prevVolume = float(volList[i-1][1])
		combined = currVolume + prevVolume
		if (combined != 0):
			diff = (currVolume - prevVolume)/combined*100
		else:
			diff = 0
		diffList.append([volList[i][0], diff])

	# Show results
	for item in diffList:
		if item[1] > 0 and item[1] > 5:
				print  symbol[0:len(symbol)-3], '[{0}] {1}%'.format('#'*int(item[1]), int(item[1]))

