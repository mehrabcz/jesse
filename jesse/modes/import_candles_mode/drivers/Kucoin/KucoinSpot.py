import requests
import jesse.helpers as jh
from jesse.modes.import_candles_mode.drivers.interface import CandleExchange
from jesse.enums import exchanges
import time
import arrow

class KucoinSpot(CandleExchange):
    def __init__(self) -> None:
        super().__init__(
            name=exchanges.KUCOIN_SPOT,
            count=60,
            rate_limit_per_second=1.5,
            backup_exchange_class=None,
            
        )

        self.endpoint = "https://api.kucoin.com"

    def get_starting_time(self, symbol: str) -> int:
        if symbol == 'SHIB-USDT':
            pass
            # payload = {
            #     'type': "1week",
            #     'symbol': symbol,
            # }
            # url = f"/api/v1/market/candles"
        
        raise AssertionError("Should not be here")
        # return super().get_starting_time(symbol)

    def fetch(self, symbol: str, start_timestamp: int, timeframe: str) -> list:
        timeframe = '1min'

        start_timestamp = int(start_timestamp / 1000)
        end_timestamp = start_timestamp + 3600
        # print(datetime.datetime.fromtimestamp(start_timestamp), datetime.datetime.fromtimestamp(end_timestamp))
        payload = {
            'type': timeframe,
            'symbol': symbol,
            'startAt': start_timestamp,
            'endAt': end_timestamp,
        }
        url = f"/api/v1/market/candles"
        url = self.endpoint + url
        # response = urlopen("https://google.com")
        # print(response)
        try:
            response = requests.get(url, params=payload)
            data = response.json()['data']
        except Exception as err:
            print(err, "sleep for 5 sec")
            time.sleep(5)
            return self.fetch(symbol, start_timestamp * 1000, '1min')

        data = [{
            'id': jh.generate_unique_id(),
            'exchange': self.name,
            'symbol': symbol,
            'timeframe': '1m',
            'timestamp': int(d[0]) * 1000,
            'open': float(d[1]),
            'close': float(d[2]),
            'high': float(d[3]),
            'low': float(d[4]),
            'volume': float(d[5])
        } for d in data]

        data = sorted(data, key=lambda x: x['timestamp'], reverse=False)
        
        return data
