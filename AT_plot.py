
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize


from AT_stock import Stock
from AT_account import Account
from AT_stock_functions import Functions




class Plot(object):

    def bind_stock(self,stockobj):
        self.stockobj = stockobj

    def bind_account(self,accountobj):
        self.accountobj = accountobj

    def bind_functions(self,f):
        self.f = f


    def fitting_function(self,x,A,B, C, w, tau):

#        return A*np.sin(x) + C

        return A*((1 + (B*(np.cos(w*x))))*np.exp((-x**2)/((2*(tau**2))))) + C

    def plot_show(self):

        fig = plt.figure()
        fig.canvas.set_window_title(str(self.stockobj.symbol))


        x_series = self.stockobj.time_num_list
        y_series_1 = self.stockobj.price_list

        ax1 = fig.add_subplot(111,xlabel = 'Time',ylabel = 'Price/EMA', xlim = (np.min(x_series), np.max(x_series)), ylim = (np.min(y_series_1), np.max(y_series_1)))



        y_series_2 = self.stockobj.EMA_1_list
        y_series_3 = self.stockobj.EMA_2_list
        y_series_4 = self.stockobj.EMA_3_list
        y_series_5 = self.stockobj.RSI_list
        y_series_6 = self.stockobj.RSI_EMA_1_list
        y_series_7 = self.stockobj.RSI_EMA_2_list
        y_series_9 = self.stockobj.volume_list



        derivative_list = []
        derivative_2_list = []
        volume_list = []
        volume_list2 = []

        for item in self.stockobj.volume_EMA_3_list:
            if not item == 0:
                volume_list.append(item)
            elif len(volume_list) > 1:
                volume_list.append(volume_list[-2])
            else:
                volume_list.append(self.stockobj.volume_EMA_3_list[-1])
        for item in self.stockobj.volume_EMA_2_list:
            if not item == 0:
                volume_list2.append(item)
            elif len(volume_list2) > 1:
                volume_list2.append(volume_list2[-2])
            else:
                volume_list2.append(self.stockobj.volume_EMA_2_list[-1])


        for item in self.stockobj.EMA_1_derivative_list:
            new_item = item * 300
            new_item += self.stockobj.price_list[1]
            derivative_list.append(new_item)
        for item in self.stockobj.EMA_1_derivative_2_list:
            new_item = item * 300
            new_item += self.stockobj.price_list[1]
            derivative_2_list.append(new_item)

        a = (self.stockobj.max_price - self.stockobj.min_price)/4

        x = np.arange(0,len(self.stockobj.ptime_list),100)


#        A = -3
#        B = -.000057
#        C = 665
#        w = 1
#        tau = -4000

        A = 1
        B = 1
        C = 1
        w = 1
        tau = 1

#        nlfit, nlpcov = scipy.optimize.curve_fit(self.fitting_function,x_series, y_series_1, p0=[A,B,C,w,tau], sigma=50)

#        A1, B1, C1, w1, tau1 = nlfit

#        fit = self.fitting_function(x_series,A1, B1, C1, w1, tau1)
        y_series_8 = derivative_list
        y_series_10 = volume_list
        y_series_11 = volume_list2
        y_series_12 = derivative_2_list

        y_series_13 = self.stockobj.f_list

        ax1.plot(x_series, y_series_1, label = "Price")
        ax1.plot(x_series, y_series_2, label = "EMA_1 ")

        ax1.plot(x_series, y_series_3, label = "EMA_2")
        ax1.plot(x_series, y_series_4, label = "EMA_3")

        plt.fill_between(x_series, y_series_2,y_series_3, color = 'grey')
        plt.fill_between(x_series, y_series_3,y_series_4, color = 'grey')



        integral_1 = self.f.calculate_Integral(y_series_1) - (self.stockobj.min_price*self.stockobj.time_num_list[-1])
        integral_2 = self.f.calculate_Integral(y_series_2) - (self.stockobj.min_price*self.stockobj.time_num_list[-1])
        integral_3 = self.f.calculate_Integral(y_series_3) - (self.stockobj.min_price*self.stockobj.time_num_list[-1])
        integral_4 = self.f.calculate_Integral(y_series_4) - (self.stockobj.min_price*self.stockobj.time_num_list[-1])




        print integral_1
        print integral_2
        print integral_3
        print integral_4


        print integral_2 - integral_3

        print integral_3 - integral_4




    #        ax1.plot(x_series, fit, label = "Fit")


        ax1.legend(loc="upper left")
#        ax2.legend(loc="lower left")

        for t in self.stockobj.buy_time_list:
            ax1.axvline(x=t,color = 'g')

        for t in self.stockobj.sell_time_list:
            ax1.axvline(x=t,color = 'r')

