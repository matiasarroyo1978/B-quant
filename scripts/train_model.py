import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
import json

def train_model(data_paths, model_path, results_path):
    data = pd.concat([pd.read_csv(path, index_col=0, parse_dates=True) for path in data_paths])

    data['RSI'] = calculate_rsi(data['Adj Close'], 14)
    data['Volatility'] = data['Adj Close'].pct_change().rolling(window=14).std()

    data = data.dropna()

    data['Target'] = (data['Adj Close'].shift(-1) > data['Adj Close']).astype(int)

    data = data.iloc[:-1]

    X = data[['Adj Close', 'RSI', 'Volatility']]
    y = data['Target']

    imputer = SimpleImputer(strategy='mean')    
    X_imputed = imputer.fit_transform(X) 

    X_imputed_df = pd.DataFrame(X_imputed, columns=X.columns)

    X_train, X_test, y_train, y_test = train_test_split(X_imputed_df, y, test_size=0.2, random_state=42)

    models = {
        'RandomForest': RandomForestClassifier(random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000),
        'SVM': SVC(probability=True),
    }

    best_model = None
    best_accuracy = 0
    results = []

    for name, model in models.items():
        print(f"Training {name} model...")

        if name == 'RandomForest':
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20],
            }
            model = GridSearchCV(model, param_grid, cv=5, scoring='accuracy')
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        print(f"{name} Model Accuracy: {accuracy * 100:.2f}%\n")
        print(classification_report(y_test, y_pred, zero_division=0))

        results.append({
            'model': name,
            'accuracy': accuracy,
            'report': pd.DataFrame(classification_report(y_test, y_pred, zero_division=0, output_dict=True)).to_dict('index')
        })


        if accuracy > best_accuracy:
            best_model = model
            best_accuracy = accuracy

    print(f"\nBest Model: {best_model.__class__.__name__}")
    print(f"Best Accuracy: {best_accuracy * 100:.2f}%")

    os.makedirs('models', exist_ok=True)
    joblib.dump(best_model, model_path)


    os.makedirs('results', exist_ok=True)
    with open(results_path, 'w') as f:
        json.dump(results, f)
    
    return best_model, imputer, results

def calculate_rsi(data, window):
    diff = data.diff(1)
    gain = diff.where(diff > 0, 0)
    loss = -diff.where(diff < 0, 0)
    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def plot_results(results):
    fig, ax = plt.subplots(1, 3, figsize=(18, 6))
    for i, result in enumerate(results):
        model_name = result['model']
        report = result['report']
        ax[i].set_title(f"{model_name} Model Performance")
        sns.heatmap(pd.DataFrame(report).iloc[:-1, :].T, annot=True, ax=ax[i])
    plt.tight_layout()
    os.makedirs('results', exist_ok=True)
    plt.savefig('results/model_performance.png')
    plt.show()

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_paths = [
        os.path.join(current_dir, '../data/datos_growth_usa.csv'),
        os.path.join(current_dir, '../data/datos_growth_eu.csv'),
        os.path.join(current_dir, '../data/datos_value_usa.csv'),
        os.path.join(current_dir, '../data/datos_value_eu.csv')
    ]
    model_path = os.path.join(current_dir, '../models/investment_model.pkl')
    results_path = os.path.join(current_dir, '../results/model_results.json')
    model, imputer, results = train_model(data_paths, model_path, results_path)
    plot_results(results)