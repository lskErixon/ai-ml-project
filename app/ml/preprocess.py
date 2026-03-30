import pandas as pd
from sklearn.preprocessing import LabelEncoder
import os

INPUT_PATH = "data/dataset/departures.jsonl"
OUTPUT_PATH = "data/processed/features.csv"


def load_data():
    print("Loading dataset...")
    df = pd.read_json(INPUT_PATH, lines=True)
    return df


def clean_data(df):
    print("Cleaning data...")

    # odstraníme řádky bez delay
    df = df.dropna(subset=["delay_min"])

    df = df[df["delay_min"] < 60]

    return df


def create_time_features(df):
    print("Creating time features...")

    df["scheduled_ts"] = pd.to_datetime(df["scheduled_ts"])
    df["hour"] = df["scheduled_ts"].dt.hour
    df["minute"] = df["scheduled_ts"].dt.minute
    df["day_of_week"] = df["scheduled_ts"].dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
    df["is_peak"] = df["hour"].isin([7, 8, 15, 16, 17]).astype(int)
    return df

def encode_categorical(df):
    print("Encoding categorical features...")

    stop_encoder = LabelEncoder()
    platform_encoder = LabelEncoder()
    headsign_encoder = LabelEncoder()

    df["stop_encoded"] = stop_encoder.fit_transform(df["source_stop"].astype(str))
    df["platform_encoded"] = platform_encoder.fit_transform(df["platform"].astype(str))
    df["headsign_encoded"] = headsign_encoder.fit_transform(df["headsign"].astype(str))
    return df

def create_final_dataset(df):
    print("Selecting final features...")
    df["route_num"] = pd.to_numeric(df["route_name"], errors="coerce")

    feature_columns = [
        "hour",
        "minute",
        "day_of_week",
        "is_weekend",
        "is_peak",
        "stop_encoded",
        "platform_encoded",
        "route_num",
        "headsign_encoded"
    ]

    df = df[feature_columns + ["delay_min"]]
    return df

def save_data(df):
    print("Saving processed data...")

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

def main():
    df = load_data()
    df = clean_data(df)
    df = create_time_features(df)
    df = encode_categorical(df)
    df = create_final_dataset(df)
    save_data(df)
    print("DONE")

if __name__ == "__main__":
    main()