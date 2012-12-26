import csv
import math
import time
import matplotlib.pyplot as plt


from AT_account import Account
from AT_stock import Stock
from AT_plot import Plot
from AT_analyze import Analyze
from AT_stock_functions import Functions

name_list = ["AAPL.quote.083112-102442"]#GOOG.quote.083112-102442"]#,"LNKD.quote.083112-102442","AAPL.quote.083112-102442"]

for name in name_list:
    file_name = "/Users/Leon/PycharmProjects/Tick Data/%s.csv" % name
    reader = csv.reader(open(file_name,"r"), delimiter=',',quotechar='"',quoting=csv.QUOTE_MINIMAL)

    stock_call_symbol = file_name[0:4]

    s = Stock(stock_call_symbol)
    ac = Account(10000)
    p = Plot()
    az = Analyze()
    f = Functions()


    s.bind_account(ac)
    ac.bind_stock(s)
    p.bind_stock(s)
    p.bind_account(ac)
    p.bind_functions(f)
    az.bind_stock(s)
    s.bind_analyze(az)
    f.bind_stock(s)
    s.bind_functions(f)


    counter = 0

    filename =  "modified" + time.strftime("%m%d%y-%H%M%S") + file_name #"%s.quote.%s.csv" % (stock_list,time.strftime("%m%d%y-%H%M%S"))

#print "starting, records will be written to %s" % filename
    print "calculating..."

#f = open(filename,"w")

    t0 = time.time()

    for row in reader:
        counter += 1
        if counter == 1: continue

        symbol = row[0]
        price = float(row[1])
        ask = float(row[2])
        bid = float(row[3])
        volume = int(row[4])
        bid_size =  int(row[5])
        ask_size = int(row[6])
        quote_time = int(row[7])
        mytime = int(row[8])
    #if symbol == "" or price == "" or mytime== "": continue

        s.update(symbol,price,ask,bid,volume,bid_size,ask_size,quote_time,mytime)
    #
        action = az.analyze()
        if action == "BUY":
            affordable_quantity = int(math.floor((ac.value - s.commission) / s.price))
            s.buy(affordable_quantity)
        elif action == "SELL":
            s.sell(s.quantity)
        elif action == "HOLD":
            pass
        else:
           raise Exception, "Unknown Action %s" % action
    #
    #
        report = "%s,%f,%f,%f,%d,%d,%d,%d,%f,%s,%f,%d" % (symbol,price,ask,bid,volume,bid_size,ask_size,quote_time,mytime,action,ac.value,s.quantity)#s.EMA_derivative)



#    print report

#f.write(report + "\n")


    if s.last_action == "BUY": s.sell_all()

    final_report = "%s: Price: %.2f, Balance: %.2f, Trades: %d" % (s.name,s.price,ac.value,s.tradenum)

    print final_report
#print "File: " + filename
#print ac.credit_list
#
#print s.upticks,s.downticks

#f.close()

    d = time.time() - t0
    n = counter / d if d > 0 else ''

    print str(counter) + " data points at " + str(n) + " pps"
    print "plotting..."


    p.plot_show()
    plt.draw()

plt.show()




