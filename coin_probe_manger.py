import threading
import logging



from upbit_class import upbit_function
from CoIn_Rect import coin_check


Buyying_Signale = False



#매도시 구매한 금액

access_key = []
secret     = []


def thread_LossCut(loss_cut):
    upbit_function()
    Target_coin_price = upbit_function.get_current_price()
    #갑자기 하한가 발생 로스컷
    if(loss_cut == Target_coin_price):
        print('긴급 Losscut 매도신호 발생')
        upbit_function.sell_market_order(access_key,secret,)
    threading.Timer(30,thread_LossCut).start()



# list [3]= False '' '' = 신호가 발생.  size = 0 TRUE

def thread_getMinCandle():
    candle = upbit_function.get_minutes_candle(upbit_function)
    Check_signal = [False,True,True]
    signal = []
    #첫 음봉 발생
    if candle == 0 and len(signal)==0:
        signal.append((True))

    #두번째 양봉 발생
    if len(signal)== 1 and candle!=2:
        if  candle ==1:
            coin_check.check_siganl(coin_check,True)
        else:
            signal.clear()
        if len(signal)==3 and signal == Check_signal:
            print('매수신호 발생')
            signal.clear()


    threading.Timer(60, thread_getMinCandle).start()










thread_getMinCandle()








