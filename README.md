# PID Delay Predictor

## Overview
PID Delay Predictor is a Python project that collects real-world public transport departure and delay data from Prague Integrated Transport (PID) using the official Golemio API.

The long-term goal of the project is to train a machine learning model that can predict delays (e.g., "delay >= 3 minutes" or "how many minutes") based on historical data.

 **Current implementation: Phase 1 — Data Collection (Crawler + Web Button)**

---

## Data pipeline
The pipeline is designed in two layers:

1) **Raw data** (original API response)  
2) **Normalized dataset** (flat records for ML)

---

## Why two outputs?
### Raw JSON (`data/raw/...`)
- stores the original API response exactly as received
- proves data origin (real-world dataset)
- useful for debugging and reproducing the dataset later

### Normalized dataset (`data/dataset/departures.jsonl`)
- stores flat ML-ready rows (1 row = 1 departure)
- stable schema for pandas / scikit-learn
- easier preprocessing and feature engineering
