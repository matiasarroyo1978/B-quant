import yfinance as yf
import ta
import os

# Función para obtener datos de Yahoo Finance
def obtener_datos(ticker, start_date, end_date):
    return yf.download(ticker, start=start_date, end=end_date)

# Función para calcular retornos acumulados
def calcular_retorno_acumulado(df):
    df['Return'] = df['Adj Close'].pct_change()
    df['Cumulative Return'] = (1 + df['Return']).cumprod()
    return df

# Función para calcular el RSI
def calcular_rsi(df, window):
    df['RSI'] = ta.momentum.RSIIndicator(df['Adj Close'], window=window).rsi()
    return df

# Configurar fechas
start_date = '2010-01-01'
end_date = '2024-01-01'

# Tickers representativos de estrategias Value y Growth para EE.UU.
tickers_value_usa = ['IWD', 'SPYV']  # Ejemplos de ETFs de Value
tickers_growth_usa = ['IWF', 'SPYG']  # Ejemplos de ETFs de Growth

# Tickers representativos de estrategias Value y Growth para Europa
tickers_value_eu = ['VGK', 'IEUR']  # Ejemplos de ETFs de Value
tickers_growth_eu = ['FEZ', 'IEUS']  # Ejemplos de ETFs de Growth

# Descargar datos
datos_value_usa = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_value_usa]
datos_growth_usa = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_growth_usa]
datos_value_eu = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_value_eu]
datos_growth_eu = [obtener_datos(ticker, start_date, end_date) for ticker in tickers_growth_eu]

# Procesar datos
datos_value_usa = [calcular_retorno_acumulado(df) for df in datos_value_usa]
datos_growth_usa = [calcular_retorno_acumulado(df) for df in datos_growth_usa]
datos_value_eu = [calcular_retorno_acumulado(df) for df in datos_value_eu]
datos_growth_eu = [calcular_retorno_acumulado(df) for df in datos_growth_eu]

# Calcular el RSI y la volatilidad para uno de los ETF de cada región
window_rsi = 14
window_volatility = 14

for df in datos_value_usa + datos_growth_usa + datos_value_eu + datos_growth_eu:
    df['RSI'] = ta.momentum.RSIIndicator(df['Adj Close'], window=window_rsi).rsi()
    df['Volatility'] = df['Adj Close'].pct_change().rolling(window=window_volatility).std()

# Guardar los datos procesados en archivos
os.makedirs('data', exist_ok=True)
datos_value_usa[0].to_csv('data/datos_value_usa.csv')
datos_growth_usa[0].to_csv('data/datos_growth_usa.csv')
datos_value_eu[0].to_csv('data/datos_value_eu.csv')
datos_growth_eu[0].to_csv('data/datos_growth_eu.csv')
