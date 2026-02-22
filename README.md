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

---

## Built With

* [![Python][Python.org]][Python-url]
* [![Flask][Flask.pallets]][Flask-url]
* [![Requests][Requests.org]][Requests-url]
* [![HTML5][HTML5.org]][HTML5-url]
* [![CSS3][CSS3.org]][CSS3-url]

<!-- MARKDOWN LINKS & IMAGES -->

[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/

[Flask.pallets]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/

[Requests.org]: https://img.shields.io/badge/Requests-2C5BB4?style=for-the-badge&logo=python&logoColor=white
[Requests-url]: https://docs.python-requests.org/

[HTML5.org]: https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white
[HTML5-url]: https://developer.mozilla.org/en-US/docs/Web/HTML

[CSS3.org]: https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS3-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
