import pandas as pd
import matplotlib.pyplot as plt
import joblib
import os
from sklearn.impute import SimpleImputer

# Cargar datos
datos_value_usa = pd.read_csv('data/datos_value_usa.csv', index_col='Date', parse_dates=True)
datos_growth_usa = pd.read_csv('data/datos_growth_usa.csv', index_col='Date', parse_dates=True)
datos_value_eu = pd.read_csv('data/datos_value_eu.csv', index_col='Date', parse_dates=True)
datos_growth_eu = pd.read_csv('data/datos_growth_eu.csv', index_col='Date', parse_dates=True)

# Función para graficar resultados
def graficar_resultados(datos_value, datos_growth, region, model, imputer):
    datos_value[['Adj Close', 'RSI', 'Volatility']] = imputer.transform(datos_value[['Adj Close', 'RSI', 'Volatility']])
    datos_growth[['Adj Close', 'RSI', 'Volatility']] = imputer.transform(datos_growth[['Adj Close', 'RSI', 'Volatility']])

    # Asegúrate de que no haya valores NaN en los datos de predicción
    datos_value['Prediction'] = model.predict(datos_value[['Adj Close', 'RSI', 'Volatility']])
    datos_growth['Prediction'] = model.predict(datos_growth[['Adj Close', 'RSI', 'Volatility']])

    # Alinear los índices de los datos
    common_index = datos_value.index.intersection(datos_growth.index)
    datos_value = datos_value.loc[common_index]
    datos_growth = datos_growth.loc[common_index]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [3, 1]})

    # Gráfico de Retornos Acumulados
    ax1.plot(datos_value.index, datos_value['Cumulative Return'], label='Retornos Value', color='magenta')
    ax1.plot(datos_growth.index, datos_growth['Cumulative Return'], label='Retornos Growth', color='orange')
    ax1.plot(datos_value.index, datos_value['Cumulative Return'] * datos_growth['Cumulative Return'], label='Estrategia Value Growth', color='green')
    ax1.set_ylabel('Retorno Acumulado')
    ax1.set_title(f'Estrategia Value Growth - {region}')
    ax1.legend(loc='upper left')

    # Gráfico del RSI
    window_rsi = 14
    ax2.plot(datos_value.index, datos_value['RSI'], label=f'RSI Indicator (Period: {window_rsi})', color='blue')
    ax2.axhline(70, color='red', linestyle='--')
    ax2.axhline(30, color='green', linestyle='--')
    ax2.set_ylabel('RSI')
    ax2.set_xlabel('Fecha')
    ax2.legend(loc='upper left')
    ax2.set_title(f'RSI - {region}')

    plt.tight_layout()

    # Ensure the output directory exists
    os.makedirs('outputs', exist_ok=True)

    plt.savefig(f'outputs/{region}_analysis.png')
    plt.show()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, '../models/investment_model.pkl')
    with open(model_path, 'rb') as f:
        model = joblib.load(f)

    imputer = SimpleImputer(strategy='mean')
    imputer.fit(pd.concat([datos_value_usa, datos_growth_usa, datos_value_eu, datos_growth_eu])[["Adj Close", "RSI", "Volatility"]])

    graficar_resultados(datos_value_usa, datos_growth_usa, 'USA', model, imputer)
    graficar_resultados(datos_value_eu, datos_growth_eu, 'EU', model, imputer)