import pandas as pd
import os
import pickle

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

INPUT_PATH = "data/processed/features.csv"
MODEL_PATH = "models/delay_model.pkl"

def load_data():
    print("Loading processed features...")
    df = pd.read_csv(INPUT_PATH)
    return df

def split_features_target(df):
    print("Splitting features and target...")
    X = df.drop(columns=["delay_min"])
    y = df["delay_min"]
    return X, y

def train_model(X_train, y_train):
    print("Training model...")

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model

def save_model(model):
    print("Saving model...")
    os.makedirs("models", exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

def main():
    df = load_data()
    X, y = split_features_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42
    )

    model = train_model(X_train, y_train)
    save_model(model)

    print("MODEL TRAINED")
    print(f"Train rows: {len(X_train)}")
    print(f"Test rows: {len(X_test)}")

if __name__ == "__main__":
    main()