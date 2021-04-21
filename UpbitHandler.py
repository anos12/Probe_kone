import pyupbit
import datetime
import time
import numpy as np
import pandas as pd
import requests
import webbrowser
from upbitpy import Upbitpy




class upbit_function:
    upbit = Upbitpy()
    target_coin =''
    INTERVAL_MIN = 1
    # 업비트 응답시간 대기


    def show_accounts(self):
        print('계좌내역-----------------')
        print(self.upbit.get_accounts())

    # 시장가 구입.
    def buy_market_order(self,coin,access_key=None, secret=None):
        upbit_ = pyupbit.Upbit(access_key,secret)
        won = pyupbit.Upbit.get_balance('KRW')
        print('%d 보유 금액',won)
        print(pyupbit.Upbit.buy_market_order(self.target_coin,won))

    #시장가 판매
    def sell_coinself(self,coin,price,access_key=None, secret=None):
        upbit_ = pyupbit.Upbit(access_key, secret)
        coins = pyupbit.Upbit.get_balance(self.target_coin)
        print(pyupbit.Upbit.sell_market_order(self.target_coin, coins))



    #현재가 조회.
    def get_current_price(self):
        pyupbit.get_current_price(self.target_coin)
        return  pyupbit.get_current_price(self.target_coin)


    def wait(min):
        now = datetime.datetime.now()
        remain_second = 60 - now.second
        remain_second += 60 * (min - (now.minute % min + 1))
        time.sleep(remain_second)
    # 타겟 코인을 찾음.
    def Serach_Target_Coin(self):
        candles_7d = dict()
        # 7일간
        krw_markets = pyupbit.get_tickers(fiat="KRW")
        print('평균 거래량 대비 60분 거래량 비율========================')
        max = -9999
        targetcoin=''
        for m in krw_markets:
            vol = self.upbit.get_minutes_candles(60, m, count=1)[0]['candle_acc_trade_volume']
            print('[{}]  (거래량:{}, )'.format(m,  format(vol, '.2f'), ))
            if vol>max:
                max=vol
                targetcoin=m
            time.sleep(0.2)
        print('거래량이 높은 타겟 코인'+targetcoin)
        self.target_coin = targetcoin
        return targetcoin
    #1분봉
    def get_minutes_candle(self):
        upbit = Upbitpy()
        print(self.target_coin)
        keys = ['opening_price', 'trade_price', 'high_price', 'low_price', 'timestamp']
        candle = self.upbit.get_minutes_candles(self.INTERVAL_MIN, self.target_coin)[0]
        print('[{}] {}'.format(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'),self.target_coin))
        for key in keys:
            print('\t{}: {}'.format(key, candle[key]))
        self.wait(self.INTERVAL_MIN)




    #스텍슬로우
    def get_market_Stochastic(self,stoch_rsi_D=None):
        url = "https://api.upbit.com/v1/candles/minutes/1"
        querystring = {"market": self.target_coin, "count": "100"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        series = df['trade_price'].iloc[::-1]
        df = pd.Series(df['trade_price'].values)

        period = 14
        smoothK = 5
        smoothD = 3

        delta = series.diff().dropna()
        ups = delta * 0
        downs = ups.copy()
        ups[delta > 0] = delta[delta > 0]
        downs[delta < 0] = -delta[delta < 0]
        ups[ups.index[period - 1]] = np.mean(ups[:period])
        ups = ups.drop(ups.index[:(period - 1)])
        downs[downs.index[period - 1]] = np.mean(downs[:period])
        downs = downs.drop(downs.index[:(period - 1)])
        rs = ups.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean() / \
             downs.ewm(com=period - 1, min_periods=0, adjust=False, ignore_na=False).mean()
        rsi = 100 - 100 / (1 + rs)

        stochrsi = (rsi - rsi.rolling(period).min()) / (rsi.rolling(period).max() - rsi.rolling(period).min())
        stochrsi_K = stochrsi.rolling(smoothK).mean()
        stochrsi_D = stochrsi_K.rolling(smoothD).mean()

        print('stoch_rsi_K: ', stochrsi_K.iloc[-1] * 100, ' percent')
        print('stoch_rsi_D: ', stochrsi_D.iloc[-1] * 100, ' percent')
        print('')
        time.sleep(1)
        return stochrsi_K, stochrsi_D
    #볼린저밴드
    def get_bollinger_bands(self):
        url = "https://api.upbit.com/v1/candles/minutes/1"
        querystring = {"market": self.target_coin, "count": "100"}
        response = requests.request("GET", url, params=querystring)
        data = response.json()
        df = pd.DataFrame(data)
        df = df['trade_price'].iloc[::-1]


        unit = 2

        band1 = unit * np.std(df[len(df) - 20:len(df)])

        bb_center = np.mean(df[len(df) - 20:len(df)])

        band_high = bb_center + band1
        band_low = bb_center - band1
        print('볼린저뱉드 상단: ', round(band_high, 2))
        print('볼린저뱉드 하단: ', round(band_low, 2))
        print('')
        time.sleep(1)
