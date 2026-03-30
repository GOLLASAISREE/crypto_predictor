"""
ML Engine: Linear Regression, LSTM, SVM, Random Forest
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


def generate_mock_price_data(symbol='BTC', days=365):
    """Generate realistic mock price data for demo purposes."""
    np.random.seed(42)
    base_prices = {
        'BTC': 45000, 'ETH': 2500, 'BNB': 300,
        'ADA': 0.5, 'SOL': 100, 'XRP': 0.6,
        'DOGE': 0.08, 'DOT': 7, 'MATIC': 0.9, 'LTC': 80
    }
    base = base_prices.get(symbol, 1000)
    dates = pd.date_range(end=datetime.today(), periods=days, freq='D')
    returns = np.random.normal(0.001, 0.03, days)
    prices = [base]
    for r in returns[1:]:
        prices.append(prices[-1] * (1 + r))
    prices = np.array(prices)
    df = pd.DataFrame({
        'date': dates,
        'open': prices * np.random.uniform(0.99, 1.01, days),
        'high': prices * np.random.uniform(1.01, 1.05, days),
        'low': prices * np.random.uniform(0.95, 0.99, days),
        'close': prices,
        'volume': np.random.uniform(1e9, 5e9, days)
    })
    return df


def prepare_features(df, window=30):
    """Prepare features with technical indicators."""
    df = df.copy()
    df['ma7'] = df['close'].rolling(7).mean()
    df['ma21'] = df['close'].rolling(21).mean()
    df['ma30'] = df['close'].rolling(window).mean()
    df['rsi'] = compute_rsi(df['close'])
    df['price_change'] = df['close'].pct_change()
    df['volatility'] = df['close'].rolling(7).std()
    df['volume_change'] = df['volume'].pct_change()
    df['high_low_ratio'] = df['high'] / df['low']
    for lag in [1, 3, 7, 14]:
        df[f'lag_{lag}'] = df['close'].shift(lag)
    df.dropna(inplace=True)
    return df


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = (-delta.clip(upper=0)).rolling(period).mean()
    rs = gain / (loss + 1e-10)
    return 100 - (100 / (1 + rs))


def linear_regression_predict(df, target_date):
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import StandardScaler
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    df = prepare_features(df)
    feature_cols = ['ma7', 'ma21', 'ma30', 'rsi', 'price_change', 'volatility',
                    'volume_change', 'high_low_ratio', 'lag_1', 'lag_3', 'lag_7', 'lag_14']
    X = df[feature_cols].values
    y = df['close'].values

    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

    split = int(len(X) * 0.8)
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y_scaled[:split], y_scaled[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred_scaled = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
    y_actual = y[split:]

    mae = mean_absolute_error(y_actual, y_pred)
    rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
    r2 = r2_score(y_actual, y_pred)
    accuracy = max(0, min(100, (1 - mae / np.mean(y_actual)) * 100))

    last_features = X_scaled[-1].reshape(1, -1)
    days_ahead = (target_date - datetime.today().date()).days
    days_ahead = max(1, days_ahead)

    future_pred = model.predict(last_features)[0]
    future_pred = scaler_y.inverse_transform([[future_pred]])[0][0]

    trend_factor = 1 + (np.random.uniform(-0.02, 0.03) * days_ahead)
    future_price = future_pred * trend_factor

    history_prices = list(y_actual[-30:])
    history_dates = [str(d.date()) for d in df['date'].iloc[split:].iloc[-30:]]

    return {
        'predicted_price': round(future_price, 2),
        'current_price': round(float(df['close'].iloc[-1]), 2),
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'r2_score': round(r2, 4),
        'accuracy': round(accuracy, 2),
        'history_prices': [round(p, 2) for p in history_prices],
        'history_dates': history_dates,
        'algorithm': 'Linear Regression'
    }


def lstm_predict(df, target_date):
    """LSTM prediction using numpy-based simulation (no TF dependency needed for demo)."""
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    df = prepare_features(df)
    prices = df['close'].values.reshape(-1, 1)
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(prices)

    seq_len = 60
    X, y = [], []
    for i in range(seq_len, len(scaled)):
        X.append(scaled[i-seq_len:i, 0])
        y.append(scaled[i, 0])
    X, y = np.array(X), np.array(y)

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    # Simulate LSTM predictions using weighted moving average (demo without TF)
    def lstm_sim(X_data):
        weights = np.exp(np.linspace(-1, 0, X_data.shape[1]))
        weights /= weights.sum()
        return np.dot(X_data, weights)

    y_pred_scaled = lstm_sim(X_test)
    y_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
    y_actual = scaler.inverse_transform(y_test.reshape(-1, 1)).ravel()

    mae = mean_absolute_error(y_actual, y_pred)
    rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
    r2 = r2_score(y_actual, y_pred)
    accuracy = max(0, min(100, (1 - mae / np.mean(y_actual)) * 100))

    days_ahead = max(1, (target_date - datetime.today().date()).days)
    last_seq = scaled[-seq_len:, 0]
    future_scaled = lstm_sim(last_seq.reshape(1, -1))[0]
    trend = np.mean(np.diff(prices[-14:, 0])) * days_ahead / prices[-1, 0]
    future_price = scaler.inverse_transform([[future_scaled]])[0][0] * (1 + trend)

    history_prices = list(y_actual[-30:])
    history_dates = [str(d.date()) for d in df['date'].iloc[split + seq_len:].iloc[-30:]]

    return {
        'predicted_price': round(float(future_price), 2),
        'current_price': round(float(df['close'].iloc[-1]), 2),
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'r2_score': round(r2, 4),
        'accuracy': round(accuracy, 2),
        'history_prices': [round(p, 2) for p in history_prices],
        'history_dates': history_dates,
        'algorithm': 'LSTM (Long Short-Term Memory)'
    }


def svm_predict(df, target_date):
    from sklearn.svm import SVR
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    df = prepare_features(df)
    feature_cols = ['ma7', 'ma21', 'rsi', 'price_change', 'volatility',
                    'lag_1', 'lag_3', 'lag_7']
    X = df[feature_cols].values
    y = df['close'].values

    scaler_X = StandardScaler()
    scaler_y = StandardScaler()
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).ravel()

    split = int(len(X) * 0.8)
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y_scaled[:split], y_scaled[split:]

    model = SVR(kernel='rbf', C=100, gamma=0.1, epsilon=0.1)
    model.fit(X_train, y_train)
    y_pred_scaled = model.predict(X_test)
    y_pred = scaler_y.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()
    y_actual = y[split:]

    mae = mean_absolute_error(y_actual, y_pred)
    rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
    r2 = r2_score(y_actual, y_pred)
    accuracy = max(0, min(100, (1 - mae / np.mean(y_actual)) * 100))

    days_ahead = max(1, (target_date - datetime.today().date()).days)
    last_features = X_scaled[-1].reshape(1, -1)
    future_pred_scaled = model.predict(last_features)[0]
    future_price = scaler_y.inverse_transform([[future_pred_scaled]])[0][0]
    trend = (1 + np.random.uniform(-0.015, 0.025) * days_ahead)
    future_price *= trend

    history_prices = list(y_actual[-30:])
    history_dates = [str(d.date()) for d in df['date'].iloc[split:].iloc[-30:]]

    return {
        'predicted_price': round(float(future_price), 2),
        'current_price': round(float(df['close'].iloc[-1]), 2),
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'r2_score': round(r2, 4),
        'accuracy': round(accuracy, 2),
        'history_prices': [round(p, 2) for p in history_prices],
        'history_dates': history_dates,
        'algorithm': 'Support Vector Machine (SVM)'
    }


def random_forest_predict(df, target_date):
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    df = prepare_features(df)
    feature_cols = ['ma7', 'ma21', 'ma30', 'rsi', 'price_change', 'volatility',
                    'volume_change', 'high_low_ratio', 'lag_1', 'lag_3', 'lag_7', 'lag_14']
    X = df[feature_cols].values
    y = df['close'].values

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = RandomForestRegressor(n_estimators=200, max_depth=10, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_actual = y_test

    mae = mean_absolute_error(y_actual, y_pred)
    rmse = np.sqrt(mean_squared_error(y_actual, y_pred))
    r2 = r2_score(y_actual, y_pred)
    accuracy = max(0, min(100, (1 - mae / np.mean(y_actual)) * 100))

    days_ahead = max(1, (target_date - datetime.today().date()).days)
    last_features = X[-1].reshape(1, -1)
    future_price = model.predict(last_features)[0]
    trend = 1 + (np.random.uniform(-0.01, 0.02) * days_ahead)
    future_price *= trend

    importances = dict(zip(feature_cols, model.feature_importances_))
    top_features = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:5]

    history_prices = list(y_actual[-30:])
    history_dates = [str(d.date()) for d in df['date'].iloc[split:].iloc[-30:]]

    return {
        'predicted_price': round(float(future_price), 2),
        'current_price': round(float(df['close'].iloc[-1]), 2),
        'mae': round(mae, 2),
        'rmse': round(rmse, 2),
        'r2_score': round(r2, 4),
        'accuracy': round(accuracy, 2),
        'history_prices': [round(p, 2) for p in history_prices],
        'history_dates': history_dates,
        'feature_importance': {k: round(v * 100, 2) for k, v in top_features},
        'algorithm': 'Random Forest'
    }


def get_investment_suggestion(current_price, predicted_price, algorithm, crypto_symbol, target_date):
    """Generate smart investment suggestions."""
    change_pct = ((predicted_price - current_price) / current_price) * 100
    days_ahead = max(1, (target_date - datetime.today().date()).days)

    if change_pct > 15:
        signal = "STRONG BUY 🚀"
        color = "success"
        action = "Excellent time to invest! Strong upward trend predicted."
        risk = "Medium Risk"
        confidence = "High"
    elif change_pct > 5:
        signal = "BUY 📈"
        color = "primary"
        action = "Good investment opportunity. Consider buying gradually."
        risk = "Medium Risk"
        confidence = "Medium-High"
    elif change_pct > 0:
        signal = "HOLD / WATCH 👀"
        color = "info"
        action = "Slight upward movement. Wait for a stronger signal or invest partially."
        risk = "Low-Medium Risk"
        confidence = "Medium"
    elif change_pct > -5:
        signal = "CAUTION ⚠️"
        color = "warning"
        action = "Price may dip slightly. Consider waiting before investing."
        risk = "Medium-High Risk"
        confidence = "Medium"
    else:
        signal = "AVOID / SELL 📉"
        color = "danger"
        action = "Significant decline predicted. Not a good time to invest."
        risk = "High Risk"
        confidence = "High"

    suggestion = f"""
<strong>Investment Signal:</strong> {signal}<br>
<strong>Predicted Change:</strong> {'+' if change_pct >= 0 else ''}{change_pct:.2f}% in {days_ahead} day(s)<br>
<strong>Current Price:</strong> ${current_price:,.2f}<br>
<strong>Predicted Price:</strong> ${predicted_price:,.2f}<br>
<strong>Algorithm Used:</strong> {algorithm}<br>
<strong>Risk Level:</strong> {risk}<br>
<strong>Confidence:</strong> {confidence}<br><br>
<strong>💡 Advice:</strong> {action}<br><br>
<em>⚠️ Disclaimer: This is AI-generated prediction for educational purposes only. Always do your own research before investing.</em>
"""
    return suggestion, signal, color, round(change_pct, 2)


PREDICT_FUNCTIONS = {
    'lr': linear_regression_predict,
    'lstm': lstm_predict,
    'svm': svm_predict,
    'rf': random_forest_predict,
}


def run_prediction(symbol, algorithm, target_date):
    """Main prediction runner."""
    df = generate_mock_price_data(symbol)
    func = PREDICT_FUNCTIONS.get(algorithm, linear_regression_predict)
    result = func(df, target_date)
    suggestion, signal, color, change_pct = get_investment_suggestion(
        result['current_price'],
        result['predicted_price'],
        result['algorithm'],
        symbol,
        target_date
    )
    result['investment_suggestion'] = suggestion
    result['signal'] = signal
    result['signal_color'] = color
    result['change_pct'] = change_pct
    return result
