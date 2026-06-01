from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import pandas as pd


# -------------------- TRAIN MODEL --------------------
def train_model(df):
    df = df.copy()

    # Convert categorical values to numeric
    df["ai_usage"] = df["ai_usage"].map({
        "Low": 1,
        "Medium": 2,
        "High": 3
    })

    df["task_complexity"] = df["task_complexity"].map({
        "Low": 1,
        "Medium": 2,
        "High": 3
    })

    # Features
    X = df[["ai_usage", "task_complexity", "time_with_ai"]]

    # Target (same logic you used)
    y = 100 - (df["time_with_ai"] * 5) - (df["errors_with_ai"] * 2)

    # Train-test split (NEW)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model (UPGRADED)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Model evaluation (NEW)
    y_pred = model.predict(X_test)
    score = r2_score(y_test, y_pred)

    return model, score


# -------------------- PREDICT --------------------
def predict_productivity(model, ai_usage, task_complexity, time_with_ai):
    input_df = pd.DataFrame([{
        "ai_usage": ai_usage,
        "task_complexity": task_complexity,
        "time_with_ai": time_with_ai
    }])

    prediction = model.predict(input_df)[0]
    return prediction