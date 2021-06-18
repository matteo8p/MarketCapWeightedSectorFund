import sys
import requests

API_KEY = 'dd73f0ab23814364a3a383a2736411e9'
sectors = [
    'Communication Services',
    'Consumer Defensive',
    'Energy',
    'Financial Services',
    'Healthcare',
    'Industrials',
    'Communication Services',
    'Technology',
    'Basic Materials',
    'Real Estate',
    'Utilities'
]

#CONFIGURATIONS
sector_weights = [
    .10,            #Communication Services
    .11,            #Consumer Defensive
    .04,            #Energy 
    .13,            #Financial Services
    .12,            #Healthcare
    .08,            #Industrials
    .10,            #Communication Services
    .22,            #Technology
    .04,            #Basic Materials
    .04,            #Real Estate
    .02             #Utilities
]
stocks_per_sector = [
    5,            #Communication Services
    5,            #Consumer Defensive
    5,            #Energy 
    5,            #Financial Services
    5,            #Healthcare
    5,             #Industrials
    5,            #Communication Services
    5,            #Technology
    5,             #Basic Materials
    5,             #Real Estate
    5             #Utilities   
]
beta_low = .5
beta_high = 5
dividend_minimum = 0
market_cap_minimum = 10000000000
supported_exchanges = ['NYSE', 'AMEX', 'NASDAQ']
blacklisted = ['GOOG']


beta = {}
dividends = {}

def init(): 
    print('Init Program')
    checkParams()
    portfolio = {}
    total_beta = 0
    total_dividend = 0

    for i in range(0, len(sectors)):
        portfolio.update(makeRequest(i))

    for stock in portfolio.keys(): 
        total_beta += beta[stock] * portfolio[stock]
        total_dividend += dividends[stock] * portfolio[stock]

    portfolio_sorted = sorted(portfolio.items(), key=lambda x: x[1], reverse=True)

    print(portfolio_sorted)
    print("Total Beta: {}".format(total_beta))
    print("Total Annual Dividends: {}".format(total_dividend))



def checkParams(): 


    print('Checking Parameter Correctness')

    #Check Sector Weight Correctness
    sector_weight_sum = 0
    for weight in sector_weights: 
        sector_weight_sum += weight

    if(sector_weight_sum != 1.0):
        raise InterruptedError('Total sector weight must equal 1.0. Current weight is {}'.format(sector_weight_sum))
    
    #Check Beta Ranges
    if beta_low < 0 or beta_high < 0:
        raise InterruptedError('Beta Range invalid. Must be greater than 0')

    #Check stocks per sector
    for num in stocks_per_sector:
        if num < 0:
            raise InterruptedError('All values in stocks per sector must be positive')
    
def makeRequest(sector_index): 
    req = 'https://financialmodelingprep.com/api/v3/stock-screener?isActivelyTrading=true&betaMoreThan={}&betaLowerThan={}&dividendMoreThan={}&marketCapMoreThan={}&sector={}&apikey={}'.format(beta_low, beta_high, dividend_minimum, market_cap_minimum, sectors[sector_index], API_KEY)
    response = requests.get(req)
    if(response.status_code != 200): 
        raise ConnectionAbortedError('API Request Error')
    json = response.json()    

    tickers = {}
    ret = {}

    for stock in json: 
        if stock['exchangeShortName'] in supported_exchanges and stock['symbol'] not in blacklisted:
            symbol = stock['symbol'].replace('-', '.')
            tickers[symbol] = stock['marketCap']
            beta[symbol] = stock['beta']
            dividends[symbol] = stock['lastAnnualDividend']
    
    sorted_tickers = sorted(tickers.items(), key=lambda x: x[1], reverse=True)[:stocks_per_sector[sector_index]]

    totalMarketCap = 0
    for stock in sorted_tickers: 
        totalMarketCap += stock[1]
    
    for i in range(0, len(sorted_tickers)): 
        ret[sorted_tickers[i][0]] = (sorted_tickers[i][1] / totalMarketCap) * sector_weights[sector_index]

    return ret


init()