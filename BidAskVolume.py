from binance.client import Client
import time
from datetime import datetime, timedelta
import argparse


parser = argparse.ArgumentParser(description='Find volume change over time for Binance tickers.')
parser.add_argument('apiKey', type=str,
                    help='your binance api key')
parser.add_argument('apiSecret', type=str,
                    help='your binance api secret')
parser.add_argument('interval', choices=['1m','3m','5m','15m','30m','1h','2h','4h','6h'],
                    help='your binance api secret')

args = parser.parse_args()

client = Client(args.apiKey, args.apiSecret)
tickers = client.get_all_tickers()
endTime = int(time.time() * 1000)
startTime = int(time.mktime((datetime.today() - timedelta(minutes=30)).timetuple()))*1000

def percentChange(candle, i, feature):
	return (float(candle[i][feature]) - float(candle[i-1][feature]))/(float(candle[i][feature]) + float(candle[i-1][feature]))*100

def totalPercent(currVal, total):
	return (float(currVal))/(float(total))*100

# Finds percent difference in between most recent candle and prior candle. Not currently used.
def incrementalChange(candleSet):
	icDict = {}
	volumeDiff = percentChange(candleSet, i,'volume')
	numTradesDiff = percentChange(candleSet, i,'numTrades')
	buyBaseVolDiff = percentChange(candleSet, i,'buyBaseVol')
	buyQuoteVolDiff = percentChange(candleSet, i,'buyQuoteVol')
	# Get percent of most recent candle relative to previous
	for i in range(1,len(candleSet)):
		currCandle = candleSet[i]
		prevCandle = candleSet[i-1]
		volumeDiff = percentChange(candleSet,i,'volume')
		numTradesDiff = percentChange(candleSet,i,'numTrades')
		buyBaseVolDiff = percentChange(candleSet,i,'buyBaseVol')
		buyQuoteVolDiff = percentChange(candleSet,i,'buyQuoteVol')

		icDict[symbol][i] = {'volumeDiff': volumeDiff, 'numTradesDiff': numTradesDiff, 
								'buyBaseVolDiff': buyBaseVolDiff,
								'buyQuoteVolDiff': buyQuoteVolDiff}
	return icDict

finalDict = {}
for ticker in tickers:
	
	symbol = ticker['symbol']

	# Only looking at BTC data
	if symbol[len(symbol)-3:len(symbol)] != 'BTC':
		continue
	candles = client.get_klines(symbol=symbol, interval=args.interval, startTime=startTime, endTime=endTime)
	finalDict[symbol] = {}
	candleSet = []
	for candle in candles:
		candleSet.append({'openTime':candle[0],
						'openPrice':candle[1],
						'highPrice':candle[2],
						'lowPrice':candle[3],
						'volume':candle[5],
						'numTrades':candle[6],
						'buyBaseVol':candle[7],
						'buyQuoteVol':candle[8]
		})

	# Get total volume to this point
	totalVolume = 0
	totalNumTrades = 0
	totalBaseVol = 0
	totalQuoteVol = 0
	for i in range(0,len(candleSet)):
		currCandle = candleSet[i]
		totalVolume += float(currCandle['volume'])
		totalNumTrades += float(currCandle['numTrades'])
		totalBaseVol += float(currCandle['buyBaseVol'])
		totalQuoteVol += float(currCandle['buyQuoteVol'])

	finalCandle = candleSet[len(candleSet) - 1]
	finalDict[symbol] = { 'volumeDiff': totalPercent(float(finalCandle['volume']), totalVolume),
							'numTradesDiff': totalPercent(float(finalCandle['numTrades']), totalNumTrades), 
							'buyBaseVolDiff': totalPercent(float(finalCandle['buyBaseVol']), totalBaseVol),
							'buyQuoteVolDiff': totalPercent(float(finalCandle['buyQuoteVol']), totalQuoteVol)
						}

# Show results
for k in finalDict.keys():
	volDiff = finalDict[k]['volumeDiff']
	if volDiff > 15:
		print "Symbol: ", k[0:len(k)-3 ]
		print '\t', '[{0}] {1}%'.format('#'*int(volDiff), int(volDiff))













