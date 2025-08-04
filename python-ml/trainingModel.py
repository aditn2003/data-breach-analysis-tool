import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import tensorflow as tf
import pymongo
import os
import joblib
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/data-breach-analysis')
client = pymongo.MongoClient(MONGO_URI)
db = client.data_breach_analysis

records = list(db.databreaches.find({}))
df = pd.DataFrame(records)

df['year'] = pd.to_datetime(df['date'])
df['records_log'] = np.log1p(df['recordsCompromised'])

X = df[['organization', 'breachType', 'year']].copy()
y = df['records_log'].values

org_encoder = LabelEncoder()
type_encoder = LabelEncoder()
X['organization'] = org_encoder.fit_transform(X['organization'].astype(str))
X['breachType'] = type_encoder.fit_transform(X['breachType'].astype(str))

scaler = StandardScaler()
X[['year']] = scaler.fit_transform(X[['year']])

X_train, X_val, y_train, y_val = train_test_split(X.values, y, test_size=0.2, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(4,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1) 
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=20, batch_size=16)

model.save("model/tf_breach_predictor.h5")
joblib.dump(org_encoder, "model/org_encoder.joblib")
joblib.dump(type_encoder, "model/type_encoder.joblib")
joblib.dump(scaler, "model/tf_scaler.joblib")

print("TensorFlow model trained and saved.")
