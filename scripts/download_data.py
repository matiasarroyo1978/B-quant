import yfinance as yf
import ta
import os

def obtener_datos(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

def calcular_retorno_acumulado(df):
    df['Return'] = df['Adj Close'].pct_change()
    df['Cumulative Return'] = (1 + df['Return']).cumprod()
    return df

def calcular_rsi(df, window):
    df['RSI'] = ta.momentum.RSIIndicator(df['Adj Close'], window=window).rsi()
    return df

start_date = '2010-01-01'
end_date = '2024-01-01'

tickers_value_usa = ['IWD', 'SPYV']  
tickers_growth_usa = ['IWF', 'SPYG']  

tickers_value_eu = ['VGK', 'IEUR']  
tickers_growth_eu = ['FEZ', 'IEUS']

datos_value_usa = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_value_usa]
datos_growth_usa = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_growth_usa]
datos_value_eu = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_value_eu]
datos_growth_eu = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_growth_eu]

datos_value_usa = [calcular_retorno_acumulado(df) for df in datos_value_usa]
datos_growth_usa = [calcular_retorno_acumulado(df) for df in datos_growth_usa]
datos_value_eu = [calcular_retorno_acumulado(df) for df in datos_value_eu]
datos_growth_eu = [calcular_retorno_acumulado(df) for df in datos_growth_eu]

window_rsi = 14
window_volatility = 14

for df in datos_value_usa + datos_growth_usa + datos_value_eu + datos_growth_eu:
    df['RSI'] = ta.momentum.RSIIndicator(df['Adj Close'], window=window_rsi).rsi()
    df['Volatility'] = df['Adj Close'].pct_change().rolling(window=window_volatility).std()

os.makedirs('data', exist_ok=True)
datos_value_usa[0].to_csv('data/datos_value_usa.csv')
datos_growth_usa[0].to_csv('data/datos_growth_usa.csv')
datos_value_eu[0].to_csv('data/datos_value_eu.csv')
datos_growth_eu[0].to_csv('data/datos_growth_eu.csv')
