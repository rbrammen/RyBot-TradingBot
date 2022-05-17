import json
import shelve
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
import time

d = shelve.open('myfile.db')
running_cash_balance = d['data'] #change to 10000 to 'reset' the running cash balance / change to d['data'] to keep running total
#print(running_cash_balance)
shares_of_voo = d['voo_shares'] #change to 0 to 'reset' the running cash balance / change to d['voo_shares'] to keep running total
#print(running_cash_balance)
d.close()

api_key = '29K8EXDWX6I2DXRM'

ts = TimeSeries(key=api_key, output_format='pandas')
data, meta_data = ts.get_daily(symbol='VOO', outputsize='compact')

closing_price_voo = data['4. close']
close_price_voo_eod = closing_price_voo[0]
close_price_voo_eod_prev = closing_price_voo[1]
#print(closing_price_voo)
print('Your cash balace is currently:', running_cash_balance)
print('You currently own', shares_of_voo, 'shares of VOO')
print('Latest EOD close price of VOO:', close_price_voo_eod)
print('Previous EOD close price of VOO:', close_price_voo_eod_prev)

def buy_voo_func():
    global sod_cash_balance
    global shares_of_voo 
    sod_cash_balance = running_cash_balance
    if shares_of_voo >= 0 and running_cash_balance > closing_price_voo[0] and closing_price_voo[0] < closing_price_voo[1]:
        sod_cash_balance = sod_cash_balance - closing_price_voo[0]
        shares_of_voo = shares_of_voo + 1
        print('You have bought 1 share of VOO today! Your cash balance is now', round(sod_cash_balance))
        print('You now have', shares_of_voo, 'shares of VOO')
    elif shares_of_voo > 0 and closing_price_voo[0] > closing_price_voo[1]:
        sod_cash_balance = sod_cash_balance + closing_price_voo[0]
        shares_of_voo = shares_of_voo - 1
        print('You have sold 1 share of VOO today! Your cash balance is now', round(sod_cash_balance))
        print('You now have', shares_of_voo, 'shares of VOO')
    elif running_cash_balance < closing_price_voo[0]:
        print('You do not have enough money to buy more VOO')
    else:
         print('You do not have any shares of VOO to sell')

buy_voo_func()

running_cash_balance = sod_cash_balance
d = shelve.open('myfile.db')
d['data'] = running_cash_balance
d['voo_shares'] = shares_of_voo
d.close() 
