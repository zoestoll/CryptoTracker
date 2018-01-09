# CryptoTracker

1. CryptoVolume.py: Very simple script to monitor incremental changes in volume for crypto tickers on Binance.

To run:

```
pip install python-binance
python CryptoVolume.py <apikey> <apiSecret> <interval>
```

Possible intervals are: 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M

2. BidAskVolume.py: Very simple script to monitor changes overall (daily) volume, number of trades, buy base volume, and quote volume, for crypto tickers on Binance. Can be modified for different time scales.

To run:

```
pip install python-binance
python BidAskVolume.py <apikey> <apiSecret> <interval>
```

Possible intervals are: 1m,3m,5m,15m,30m,1h,2h,4h,6h

