import json
import os
import shelve
import time

from alpha_vantage.timeseries import TimeSeries

try:
    ALPHA_VANTAGE_API_KEY = os.environ['ALPHA_VANTAGE_API_KEY']
except KeyError:
    raise RuntimeError('ALPHA_VANTAGE_API environmental variable not set, aborting')

def get_cash_and_shares():
    with shelve.open('myfile.db') as database:
        running_cash_balance = database['data'] #change to 10000 to 'reset' the running cash balance / change to d['data'] to keep running total
        shares_of_voo = database'voo_shares'] #change to 0 to 'reset' the running cash balance / change to d['voo_shares'] to keep running total
        return running_cash_balance, shares

def save_cash_and_shares(running_cash_balance, shares):
    with shelve.open('myfile.db') as database:
        database['data'] = running_cash_balance
        database['voo_shares'] = shares_of_voo
    
def get_voo_prices():
    ts = TimeSeries(key=ALPHA_VANTAGE_API_KEY, output_format='pandas')
    data, meta_data = ts.get_daily(symbol='VOO', outputsize='compact')
    closing_price_voo = data['4. close']
    close_price_voo_eod = closing_price_voo[0]
    close_price_voo_eod_prev = closing_price_voo[1]
    return close_price_voo_eod, close_price_voo_eod_prev

def buy_or_sell_voo(cash_balance, shares_of_voo, close_price_voo_eod, close_price_voo_eod_prev):
    if shares_of_voo >= 0 and cash_balance > close_price_voo_eod and close_price_voo_eod < close_price_voo_eod_prev:
        cash_balance -= close_price_voo_eod
        shares_of_voo += 1
        print('You have bought 1 share of VOO today! Your cash balance is now', round(cash_balance))
        print('You now have', shares_of_voo, 'shares of VOO')
    elif shares_of_voo > 0 and close_price_voo_eod > close_price_voo_eod_prev:
        cash_balance += close_price_voo_eod
        shares_of_voo -= 1
        print('You have sold 1 share of VOO today! Your cash balance is now', round(cash_balance))
        print('You now have', shares_of_voo, 'shares of VOO')
    elif cash_balance < close_price_voo_eod:
        print('You do not have enough money to buy more VOO')
    else:
        print('You do not have any shares of VOO to sell')
    return cash_balance, shares_of_voo

if __name__ == "__main__":
    cash, shares = get_cash_and_shares()
    close_price_voo_eod, close_price_voo_eod_prev = get_voo_prices()
    cash, shares = buy_or_sell_voo(cash, shares, close_price_voo_eod, close_price_voo_eod_prev )

    print('Your cash balace is currently:', cash)
    print('You currently own', shares, 'shares of VOO')
    print('Latest EOD close price of VOO:', close_price_voo_eod)
    print('Previous EOD close price of VOO:', close_price_voo_eod_prev)

    save_cash_and_shares(cash, shares)
