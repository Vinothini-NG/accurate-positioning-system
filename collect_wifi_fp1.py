import sqlite3
import subprocess
import re
import time

def scan_wifi():
    command = "netsh wlan show networks mode=bssid"
    result = subprocess.check_output(command, shell=True, encoding='utf-8', errors='ignore')
    bssids = re.findall(r'BSSID\s+\d+\s*:\s*([\w:]+)', result)
    signals = re.findall(r'Signal\s*:\s*(\d+)%', result)
    wifi_data = []
    for bssid, signal in zip(bssids, signals):
        rssi = int(signal) // 2 - 100
        wifi_data.append((bssid, rssi))
    return wifi_data

def collect_fingerprints(zone, num_samples=10):
    conn = sqlite3.connect("zone_fingerprints.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS fingerprints (
                    bssid TEXT,
                    rssi INTEGER,
                    zone TEXT)""")
    
    for i in range(num_samples):
        print(f"📶 Sample {i+1}/{num_samples}")
        wifi_data = scan_wifi()
        for bssid, rssi in wifi_data:
            c.execute("INSERT INTO fingerprints (bssid, rssi, zone) VALUES (?, ?, ?)", (bssid, rssi, zone))
        conn.commit()
        time.sleep(1.5)

    conn.close()
    print(f"\n✅ Collected {num_samples} samples for zone '{zone}'")

if __name__ == "__main__":
    zone = input("Enter zone name (e.g., Room A, Room B): ")
    collect_fingerprints(zone)
