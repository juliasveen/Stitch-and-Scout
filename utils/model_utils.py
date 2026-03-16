import pandas as pd
import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

def retrain_model():
    df = pd.read_csv("dataset.csv")

    # Keep only the last 5000 records to save RAM
    if len(df) > 5000:
        df = df.tail(5000)

    if len(df) < 10:
        print("⚠️  Not enough data to train. Run sync_market.py first.")
        return

    X = df[["brand", "type", "condition", "size", "material"]]
    y = df["price"]

    preprocessor = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"),
         ["brand", "type", "condition", "size", "material"])
    ])

    model = Pipeline([
        ("prep", preprocessor),
        ("reg", RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    model.fit(X, y)
    joblib.dump(model, "price_model.pkl")
    print(f"✅ Model retrained on {len(df)} records and saved to price_model.pkl")
