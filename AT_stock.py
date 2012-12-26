import math
import numpy as np


from AT_analyze import Analyze

class Stock(object):
    def __init__(self,name):
        self.name = name

        # Data Variables

        self.price = None
        self.symbol = None
        self.ptime = None
        self.qtime = None
        self.ask = None
        self.bid = None
        self.ask_size = None
        self.bid_size = None
        self.volume = 0
        self.volume_list = np.array([])
        self.real_volume = None
        self.price_history = np.array([])
        self.price_list = []
        self.change_history = np.array([])
        self.quantity = 0
        self.ptime_list = np.array([])
        self.qtime_list = np.array([])
        self.volume_EMA_1= 0
        self.volume_EMA_2= 0
        self.volume_EMA_3= 0
        self.volume_EMA_1_list = []
        self.volume_EMA_2_list =np.array([])
        self.volume_EMA_3_list = np.array([])

        # Monetary Variables

        self.accountobj = None
        self.purchase = None
        self.current_value = None
        self.commission = 10
        self.tradenum = 0
        self.transactions = {}
        self.last_transaction = {}
        self.last_transaction_time = 1
        self.profit_price = None
        self.price_range = None
        self.min_price = None
        self.max_price = None
        self.purchase_price = None
        self.price_range_ratio = None
        self.last_buy_time = 1
        self.last_action = None
        self.ask_list = []
        self.moving_avg = None
        self.moving_avg_list = []
        self.profit_price_list = []
        self.buy_time = None
        self.sell_time = None
        self.buy_time_list = []
        self.sell_time_list = []
        self.MACD_list = []

        # EMA Variables

        self.EMA_1 = None
        self.EMA_1_list = []
        self.EMA_1_derivative_list = []
        self.EMA_1_derivative = None
        self.EMA_2_derivative = None

        self.EMA_1_derivative_2 = None
        self.EMA_1_derivative_2_list = []

        self.EMA_2 = None
        self.EMA_2_list = []

        self.EMA_3 = None
        self.EMA_3_list = []
        self.EMA_3_derivative = None


        self.EMA_1_multiplier = .002
        self.EMA_2_multiplier = .002
        self.EMA_3_multiplier = .001

        self.EMA_1_slope_min = None
        self.EMA_2_slope_min = None
        self.EMA_3_slope_min = None

        self.f = 0
        self.f_list = []

        # RSI Variables

        self.RSI = 50
        self.RSI_list = []

        self.gain = None
        self.loss = None

        self.RSI_EMA_1 = 50
        self.RSI_EMA_2 = 50
        self.RSI_EMA_3 = 50
        self.RSI_EMA_1_list = []
        self.RSI_EMA_2_list = []
        self.RSI_EMA_3_list = []

        self.time_num = 0
        self.time_num_list = []

        self.RSI_EMA_derivative = None
        self.RSI_EMA_derivative_list = []

        self.RSI_EMA_2_derivative = None
        self.RSI_EMA_2_derivative_list = []

        self.RSI_EMA_2 = None
        self.RSI_EMA_2_list = []

        self.gain_list = []
        self.loss_list = []

        self.prev_gain_list = []
        self.prev_loss_list = []

    def bind_account(self,accountobj):
        self.accountobj = accountobj

    def bind_functions(self,f):
        self.f = f

    def bind_analyze(self,az):
        self.az = az

    def update(self,symbol,price,ask,bid,volume,bid_size,ask_size,qtime,ptime):

        self.symbol = symbol

        # Prices Variables

        self.price = float(price)
        self.price_list.append(self.price)


        self.ask = ask
        self.ask_list.append(self.ask)
        self.ask_size = ask_size

        self.bid = bid
        self.bid_size = bid_size

        self.min_price = self.price if (self.min_price == None or self.price < self.min_price) else self.min_price
        self.max_price = self.price if (self.max_price == None or self.price > self.max_price) else self.max_price
        self.price_range = self.max_price - self.min_price
        self.price_range_ratio = self.price_range/self.price

        # Volume Calculation

        self.volume = volume

        if len(self.volume_list) < 2:
            np.append(self.volume_list,self.volume)
            self.real_volume = sum(self.volume_list)
        elif not self.volume == self.volume_list[-2]:
            np.append(self.volume_list,self.volume)
            self.real_volume = sum(self.volume_list)
        else:
            self.volume_list.append(0)

        # Time Variables
        self.qtime = qtime
        np.append(self.qtime_list,self.qtime)

        self.ptime = ptime
        np.append(self.ptime_list,self.ptime)

        self.time_num += 1
        self.time_num_list.append(self.time_num)

        # Implementing Indicator Methods
        #        self.calculate_RSI()

        self.f.EMA()
#        self.derivative()
        self.f.calculate_function()



    def buy(self,quantity):
        amount = self.price * quantity
        if self.accountobj.value < amount:
            affordable_quantity = int(math.floor((self.accountobj.value-self.commission) / self.price))
            if affordable_quantity < 1:
                raise Exception, "Insufficient Funds"
            else:
                quantity = affordable_quantity
                amount = self.price * quantity

        self.quantity += float(quantity)
        self.accountobj.debit(amount)
        self.tradenum += 1
        self.last_transaction = {self.ptime : {'Action':'BUY','Price':self.price,'Quantity':self.quantity}}

        self.transactions[self.ptime] =  {'Action':'BUY','Price':self.price,'Quantity':self.quantity}

        self.last_transaction_time = self.ptime

        self.last_buy_time = self.ptime

        self.profit_price = ((self.price * self.quantity) + self.commission)/self.quantity

        self.purchase_price = self.price

        self.buy_time_list.append(self.time_num)

    def sell(self,quantity):
        amount = self.price * quantity
        if self.quantity < quantity:
            raise Exception,"Sell order too large."
        self.quantity -= float(quantity)
        self.accountobj.credit(amount)
        self.tradenum += 1

        self.last_transaction = {self.ptime : {'Action':'SELL','Price':self.price,'Quantity':self.quantity}}

        self.transactions[self.ptime] =  {'Action':'SELL','Price':self.price,'Quantity':self.quantity}

        self.last_transaction_time = self.ptime


        self.sell_time_list.append(self.time_num)#self.ptime

    def buy_all(self):
        affordable_quantity = int(math.floor(((self.accountobj.value - self.commission) / self.price)))
        self.buy(affordable_quantity)
        self.quantity = affordable_quantity
        self.purchase = (self.price * self.quantity)

    def sell_all(self):
        self.sell(self.quantity)

