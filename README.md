Accurate Positioning System
A Wi-Fi fingerprinting-based indoor positioning system designed to accurately determine a user's location within indoor environments where GPS signals are unreliable.

📌 Overview
This project leverages Wi-Fi signal strength data to create a fingerprinting model that predicts the user's location within a predefined indoor space.

🗂️ Project Structure
1.collect_wifi_fp1.py: Script to collect Wi-Fi signal strength data and store it in a SQLite database.
2.train_model.py: Trains a machine learning model (e.g., Random Forest) using the collected Wi-Fi fingerprints.
3.predict.py: Uses the trained model to predict the current location based on real-time Wi-Fi data.
4.server.py: Runs a Flask web server to serve the prediction results.
5.sql.py: Handles database operations for storing and retrieving Wi-Fi fingerprints.
6.templates/: Contains HTML templates for the web interface.
7.zone_fingerprints.db: SQLite database storing the collected Wi-Fi fingerprints.
8.zone_predictor_rf_model.joblib: Serialized machine learning model for location prediction.


**Prerequisites**
Python 3.11.0

**Required Python packages:**

1.Flask
2.scikit-learn
3.joblib
4.sqlite3

**Installation**
Clone the repository:
git clone https://github.com/Vinothini-NG/accurate-positioning-system.git

cd accurate-positioning-system

**Install the required packages:**
pip install -r requirements.txt

1.First, run the collect_wifi_fp1.py script. It will start collecting Wi-Fi fingerprint samples from nearby access points.

2.Next, run train_model.py to train the model using the collected fingerprint data.

3.Then, run predict.py, which will predict the user's current position based on real-time Wi-Fi signals.

4.Finally, start the server by running server.py. Access the web interface at http://localhost:5000 to view the predicted location.
