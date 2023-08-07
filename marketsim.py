import datetime as dt
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def compute_portvals(  		  	   		  		 			  		 			     			  	 
    orders_file="./orders/orders.csv",  		  	   		  		 			  		 			     			  	 
    start_val=1000000,
    commission=9.95,  		  	   		  		 			  		 			     			  	 
    impact=0.005,  		  	   		  		 			  		 			     			  	 
):
    """  		  	   		  		 			  		 			     			  	 
    Computes the portfolio values.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		  		 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		  		 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
    :type start_val: int  		  	   		  		 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		  		 			  		 			     			  	 
    """
    # this is the function the autograder will call to test your code  		  	   		  		 			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		  		 			  		 			     			  	 
    # code should work correctly with either input  		  	   		  		 			  		 			     			  	 
    # TODO: Your code here

    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    start_date = orders_df.index.min()
    end_date = orders_df.index.max()
    orders_dates = orders_df.index

    symbols = {}
    shares_delivery = {}
    cash = start_val

    portvals = get_data(['SPY'], pd.date_range(start_date, end_date), addSPY=True, colname='Adj Close')
    portvals = portvals.rename(columns={'SPY': 'value'})
    dates = portvals.index

    for date in dates:
        if date in orders_dates:
            details = orders_df.loc[date]
            if isinstance(details, pd.DataFrame):
                for _, each in details.iterrows():
                    symbol = each.loc['Symbol']
                    order = each.loc['Order']
                    shares = each.loc['Shares']
                    cash, shares_delivery, symbols = update_cash(symbol, order, shares, cash, shares_delivery, symbols, date,
                                    end_date, commission, impact)
            else:
                symbol = details.loc['Symbol']
                order = details.loc['Order']
                shares = details.loc['Shares']
                cash, shares_delivery, symbols = update_cash(symbol, order, shares, cash, shares_delivery, symbols, date, end_date,
                                commission, impact)
        shares_value = 0
        for symbol in shares_delivery:
            shares_value += symbols[symbol].loc[date].loc[symbol] * shares_delivery[symbol]
        portvals.loc[date].loc['value'] = cash + shares_value

        # if np.isnan(portvals.iloc[0]):
        #     raise ValueError('Portfolio values cannot be NaNs!')

    return portvals


def update_cash(symbol, order, shares, cash, shares_delivery, symbols, date, end_date, commission,
                impact):
    if symbol not in symbols:
        symbol_df = get_data([symbol], pd.date_range(date, end_date), addSPY=True, colname='Adj Close')
        symbol_df.fillna(method='ffill', inplace=True)
        symbol_df.fillna(method='bfill', inplace=True)
        symbols[symbol] = symbol_df

    if order == 'BUY':
        share_diff = shares
        cash_diff = -symbols[symbol].loc[date].loc[symbol] * (1 + impact) * shares
    elif order == 'SELL':
        share_diff = -shares
        cash_diff = symbols[symbol].loc[date].loc[symbol] * (1 - impact) * shares
    else:
        print('Invalid Order')
    shares_delivery[symbol] = shares_delivery.get(symbol, 0) + share_diff
    cash += cash_diff - commission
    return cash, shares_delivery, symbols


def author():
  return 'aishwary'

  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Helper function to test code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		  		 			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		  		 			  		 			     			  	 
    # Define input parameters  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    of = "./orders/orders2.csv"  		  	   		  		 			  		 			     			  	 
    sv = 1000000  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Process orders  		  	   		  		 			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)
    if isinstance(portvals, pd.DataFrame):  		  	   		  		 			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  		 			  		 			     			  	 
    else:  		  	   		  		 			  		 			     			  	 
        "warning, code did not return a DataFrame"  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Get portfolio stats  		  	   		  		 			  		 			     			  	 
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		  		 			  		 			     			  	 
    start_date = dt.datetime(2008, 1, 1)  		  	   		  		 			  		 			     			  	 
    end_date = dt.datetime(2008, 6, 1)  		  	   		  		 			  		 			     			  	 
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		  		 			  		 			     			  	 
        0.2,  		  	   		  		 			  		 			     			  	 
        0.01,  		  	   		  		 			  		 			     			  	 
        0.02,  		  	   		  		 			  		 			     			  	 
        1.5,  		  	   		  		 			  		 			     			  	 
    ]  		  	   		  		 			  		 			     			  	 
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		  		 			  		 			     			  	 
        0.2,  		  	   		  		 			  		 			     			  	 
        0.01,  		  	   		  		 			  		 			     			  	 
        0.02,  		  	   		  		 			  		 			     			  	 
        1.5,  		  	   		  		 			  		 			     			  	 
    ]  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Compare portfolio against $SPX  		  	   		  		 			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
