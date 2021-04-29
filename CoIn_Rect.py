

class coin_check:
   # Check_Signal =[] #Kone 알고리즘
   # CoinName         #코인이름
   # BidSpread        #매도가
   # AskSpread        #매수가
   # BidSpreadTime    #매도시간
   # AskSpreadTime    #매수시간


    def __init__(self):
        self.Check_Signals =[]
        self.top= -1
        self.size =0
        self.max_size = 3


    def push(self, item):
        if self.max_size < self.size:
            self.Check_Signals.append(item)
            self.size = self.size + 1
            self.top = self.top + 1
        else:
            raise ValueError('max size limit exceeded')

    def pop(self):
         if self.isEmpty():
            return None
         else:
            self.ret = self.Check_Signals.pop(self.top)
            self.size = self.top - 1
            self.top = self.top - 1
            return self.ret

    def peek(self):
        if self.isEmpty():
            return None
        else:
            return self.Check_Signals[self.top]

    def check_siganl(self):

        Check_list = [False,True,True]
        # 음봉->양봉->양봉 때 매수신호 발생.
        if(Check_Signal==Check_list):
         return True
        else:
         return False


    def getCoinListSize(self):
        return self.size




