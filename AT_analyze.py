
import numpy as np


class Analyze(object):

    def bind_stock(self,s):
        self.s = s

    def analyze(self):

        affordable_quantity = int(np.floor(((self.s.accountobj.value-self.s.commission) / self.s.price)))

        if self.s.last_transaction.has_key(self.s.last_transaction_time):
            self.s.last_action = self.s.last_transaction[self.s.last_transaction_time]['Action']
        else:
            self.s.last_action = "HOLD"

        while self.s.accountobj.value + (self.s.price * self.s.quantity) > self.s.accountobj.init_value * .9:
            while self.s.last_action == 'BUY' :
                if self.convergence() is True:
                    return "SELL"
                else:
                    return "HOLD"

            while self.s.last_action == 'SELL' or self.s.last_action == 'HOLD'  :
                if len(self.s.EMA_1_list) > 50 and self.convergence() is True:# or ((self.EMA_list[-1] > self.EMA_2_list[-1] and (self.EMA < self.EMA_2))):#round(self.EMA,4) == round (self.EMA_2,4) or round(self.EMA,5) == round (self.EMA_2 or round(self.EMA,6) == round (self.EMA_2:#(sum(x < 0 for x in self.EMA_derivative_list[-600:-200]) == 400 and sum(x > 0 for x in self.EMA_derivative_list[-200:]) == 200) or sum(x > 0 for x in self.EMA_derivative_list[-400:]) == 400:
                    return "BUY"
                else:
                    return "HOLD"
        else:
            return "HOLD"

    def convergence(self):

        if self.s.last_action == "BUY" and (self.s.EMA_1_list[-2] > self.s.EMA_2_list[-2]) and (self.s.EMA_1 < self.s.EMA_2): #downwards convergence
            return True

        if self.s.last_action != "BUY" and ((self.s.EMA_1_list[-2] < self.s.EMA_2_list[-2] and (self.s.EMA_1 > self.s.EMA_2))): #upwards convergence
            return True

        else:
            return False