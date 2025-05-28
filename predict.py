import subprocess
import re
import sqlite3
import pandas as pd
import joblib
from collections import deque
from statistics import mode

# Load trained model
clf = joblib.load("zone_predictor_rf_model.joblib")

# Prediction smoothing buffer
prediction_buffer = deque(maxlen=10)

# Scan Wi-Fi networks using netsh (Windows)
def scan_wifi():
    command = "netsh wlan show networks mode=bssid"
    try:
        result = subprocess.check_output(command, shell=True, encoding='utf-8', errors='ignore')
    except subprocess.CalledProcessError as e:
        print("❌ Error running Wi-Fi scan:", e)
        return {}

    bssids = re.findall(r'BSSID\s+\d+\s*:\s*([\w:]+)', result)
    signals = re.findall(r'Signal\s*:\s*(\d+)%', result)

    wifi_data = {}
    for bssid, signal in zip(bssids, signals):
        rssi = int(signal) // 2 - 100  # Convert % to approximate dBm
        wifi_data[bssid] = rssi

    return wifi_data

# Normalize signal strength (optional — only if model was trained with normalized features)
def normalize_signals(wifi_dict):
    if not wifi_dict:
        return {}
    min_rssi = min(wifi_dict.values())
    max_rssi = max(wifi_dict.values())
    if min_rssi == max_rssi:
        return {bssid: 50.0 for bssid in wifi_dict}  # flat value if no variance
    return {
        bssid: (rssi - min_rssi) / (max_rssi - min_rssi) * 100
        for bssid, rssi in wifi_dict.items()
    }

# Log any unknown BSSIDs not seen during training
def log_unknown_bssids(wifi_dict):
    known_bssids = set(clf.feature_names_in_)
    unknowns = [b for b in wifi_dict if b not in known_bssids]
    if unknowns:
        print(f"⚠️ Unseen BSSIDs: {unknowns}")

# Predict current zone using the trained model
def predict_zone_smooth(wifi_dict):
    all_bssids = clf.feature_names_in_
    row = {bssid: wifi_dict.get(bssid, -100) for bssid in all_bssids}
    df = pd.DataFrame([row])
    pred = clf.predict(df)[0]
    prediction_buffer.append(pred)

    # Return the most frequent prediction in the buffer
    return mode(prediction_buffer)

# Main workflow
def navigate():
    print("📡 Scanning Wi-Fi to detect current location...")
    wifi_dict = scan_wifi()

    if not wifi_dict:
        print("❌ No Wi-Fi data found. Try again.")
        return

    # Optional: Normalize signals (only if model was trained with normalized RSSI)
    # wifi_dict = normalize_signals(wifi_dict)

    log_unknown_bssids(wifi_dict)
    current_zone = predict_zone_smooth(wifi_dict)
    print(f"📍 Detected current zone: {current_zone}")

if __name__ == "__main__":
    navigate()
