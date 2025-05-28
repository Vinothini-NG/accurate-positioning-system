import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
import joblib

# Connect to SQLite DB and load data
conn = sqlite3.connect("zone_fingerprints.db")
df = pd.read_sql_query("SELECT bssid, rssi, zone FROM fingerprints", conn)
conn.close()

# Add a sample_id (unique for each fingerprint set)
df['sample_id'] = df.groupby(['zone']).cumcount()

# Create pivot table: one row per sample, one column per BSSID
pivoted = df.pivot_table(index='sample_id', columns='bssid', values='rssi', aggfunc='mean').fillna(-100)

# Add the zone labels back in
pivoted['zone'] = df.groupby('sample_id')['zone'].first().values

# Separate features and target
X = pivoted.drop(columns='zone')
y = pivoted['zone']

# Normalize RSSI values
scaler = MinMaxScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, stratify=y, random_state=42)

# Train Random Forest
clf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
clf.fit(X_train, y_train)

# Evaluate model
y_pred = clf.predict(X_test)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, zero_division=1))

# Save the model
joblib.dump(clf, "zone_predictor_rf_model.joblib")
print("\n✅ Model saved as 'zone_predictor_rf_model.joblib'")
