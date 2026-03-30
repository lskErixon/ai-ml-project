import pandas as pd
import pickle

from sklearn.metrics import mean_absolute_error, mean_squared_error

INPUT_PATH = "data/processed/features.csv"
MODEL_PATH = "models/delay_model.pkl"

def load_data():
    print("Loading data...")
    df = pd.read_csv(INPUT_PATH)
    return df

def load_model():
    print("Loading model...")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

def evaluate():
    df = load_data()
    model = load_model()

    X = df.drop(columns=["delay_min"])
    y = df["delay_min"]

    print("Predicting...")
    y_pred = model.predict(X)

    mae = mean_absolute_error(y, y_pred)
    mse = mean_squared_error(y, y_pred)

    print("\n=== RESULTS ===")
    print(f"MAE: {mae}")
    print(f"MSE: {mse}")

    print("\nExample predictions:")
    for i in range(5):
        print(f"Real: {y.iloc[i]} min | Predicted: {round(y_pred[i], 2)} min")

if __name__ == "__main__":
    evaluate()