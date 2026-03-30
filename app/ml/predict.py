import pickle
import pandas as pd

MODEL_PATH = "models/delay_model.pkl"

def load_model():
    print("Loading model...")
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model

def predict_delay(model, features: dict):
    df = pd.DataFrame([features])
    prediction = model.predict(df)[0]
    return prediction

def main():
    model = load_model()

    # testovací vstup
    sample = {
        "hour": 9,
        "minute": 13,
        "day_of_week": 0,
        "is_weekend": 0,
        "is_peak": 1,
        "stop_encoded": 0,
        "platform_encoded": 0,
        "route_num": 2,
        "headsign_encoded": 0
    }

    pred = predict_delay(model, sample)
    print("PREDICTION")
    print(f"Predicted delay: {round(pred, 2)} min")

if __name__ == "__main__":
    main()