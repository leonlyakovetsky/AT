

class Account(object):
    def __init__(self,init_value):
        self.init_value = init_value
        self.value = self.init_value
        self.credit_list = [self.value]
        self.debit_list = [self.value]
        self.last_credit = self.value
        self.last_debit = self.value

    def bind_stock(self,stockobj):
        self.stockobj = stockobj

    def credit(self,value):
        '''add money to account'''
        self.value += (value - self.stockobj.commission)
        self.credit_list.append(self.value)
        self.last_credit = self.value

    def debit(self,value):
        '''take money from account'''
        self.value -= (value + self.stockobj.commission)
        self.debit_list.append(self.value)
        self.last_debit = self.value