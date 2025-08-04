from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from dotenv import load_dotenv
import pymongo
from datetime import datetime
import json
import tensorflow as tf

load_dotenv()

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/data-breach-analysis')
client = pymongo.MongoClient(MONGO_URI)
db = client.data_breach_analysis

model = None
label_encoders = {}
scaler = None
tf_model = None
industry_encoder = None
type_encoder = None
tf_scaler = None

def load_tf_model():
    global tf_model, industry_encoder, type_encoder, tf_scaler
    try:
        tf_model = tf.keras.models.load_model("model/tf_breach_predictor.h5")
        industry_encoder = joblib.load("model/org_encoder.joblib")
        type_encoder = joblib.load("model/type_encoder.joblib")
        tf_scaler = joblib.load("model/tf_scaler.joblib")
        print("TensorFlow model and encoders loaded.")
    except Exception as e:
        print("Failed to load TensorFlow model:", e)

def load_or_train_model():
    """Load existing model or train a new one"""
    global model, label_encoders, scaler
    
    model_path = 'models/breach_predictor.joblib'
    encoders_path = 'models/label_encoders.joblib'
    scaler_path = 'models/scaler.joblib'
    
    os.makedirs('models', exist_ok=True)
    
    try:
        model = joblib.load(model_path)
        label_encoders = joblib.load(encoders_path)
        scaler = joblib.load(scaler_path)
        print("Loaded existing model")
    except FileNotFoundError:
        print("Training new model...")
        train_model()
        print("Model training completed")

def train_model():
    """Train the machine learning model"""
    global model, label_encoders, scaler
    
    breaches = list(db.databreaches.find({}))
    
    if len(breaches) < 10:
        breaches = create_synthetic_data()
    
    df = pd.DataFrame(breaches)
    
    df['year'] = pd.to_datetime(df['date']).dt.year
    df['month'] = pd.to_datetime(df['date']).dt.month
    df['records_log'] = np.log1p(df['recordsCompromised'])
    
    features = ['organization', 'breachType', 'year', 'month']
    X = df[features].copy()
    y = df['records_log']
    
    label_encoders = {}
    for col in ['organization', 'breachType']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
    
    scaler = StandardScaler()
    numerical_features = ['year', 'month']
    X[numerical_features] = scaler.fit_transform(X[numerical_features])
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    joblib.dump(model, 'models/breach_predictor.joblib')
    joblib.dump(label_encoders, 'models/label_encoders.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')

def create_synthetic_data():
    """Create synthetic data for demonstration"""
    organizations = ['TechCorp', 'BankSecure', 'HealthData', 'EduNet', 'RetailChain']
    breach_types = ['Hacking', 'Phishing', 'Malware', 'Insider', 'Physical']
    
    synthetic_data = []
    for i in range(100):
        org = np.random.choice(organizations)
        breach_type = np.random.choice(breach_types)
        year = np.random.randint(2015, 2024)
        month = np.random.randint(1, 13)
        records = np.random.randint(1000, 10000000)
        
        synthetic_data.append({
            'organization': org,
            'breachType': breach_type,
            'date': f"{year}-{month:02d}-01",
            'recordsCompromised': records
        })
    
    return synthetic_data

def predict_breach_risk(organization, breach_type, year):
    """Predict breach risk for given parameters"""
    if model is None:
        return None

    input_data = pd.DataFrame({
        'organization': [organization],
        'breachType': [breach_type],
        'year': [year],
        'month': [6]  
    })

    for col, le in label_encoders.items():
        if col in input_data.columns:
            val = input_data[col].iloc[0]

            if val not in le.classes_:
                le.classes_ = np.append(le.classes_, val)
            
            input_data[col] = le.transform([val])

    numerical_features = ['year', 'month']
    input_data[numerical_features] = scaler.transform(input_data[numerical_features])

    input_data = input_data.astype(float)
   
    predicted_log = model.predict(input_data)[0]
    predicted_records = np.expm1(predicted_log)

    historical_breaches = list(db.databreaches.find({
        'organization': {'$regex': organization, '$options': 'i'},
        'breachType': breach_type
    }))

    if historical_breaches:
        avg_records = np.mean([b['recordsCompromised'] for b in historical_breaches])
        risk_score = min(100, (predicted_records / avg_records) * 50)
    else:
        risk_score = min(100, predicted_records / 1_000_000 * 100)

    confidence = min(0.95, 0.5 + len(historical_breaches) * 0.1)

    return {
        'predictedRisk': risk_score,
        'confidence': confidence,
        'predictedRecords': int(predicted_records),
        'factors': [
            'historical_trends',
            'organization_size',
            'breach_type_frequency',
            'year_trend'
        ],
        'recommendations': generate_recommendations(risk_score, breach_type)
    }


def generate_recommendations(risk_score, breach_type):
    """Generate security recommendations based on risk score and breach type"""
    recommendations = []
    
    if risk_score > 70:
        recommendations.extend([
            'Implement immediate security audit',
            'Upgrade authentication systems',
            'Deploy advanced threat detection',
            'Conduct employee security training'
        ])
    elif risk_score > 40:
        recommendations.extend([
            'Review security protocols',
            'Implement stronger authentication',
            'Regular security assessments',
            'Employee awareness training'
        ])
    else:
        recommendations.extend([
            'Maintain current security measures',
            'Regular security monitoring',
            'Keep systems updated',
            'Periodic security reviews'
        ])
    
    if breach_type == 'Hacking':
        recommendations.append('Implement network segmentation')
    elif breach_type == 'Phishing':
        recommendations.append('Deploy email security solutions')
    elif breach_type == 'Malware':
        recommendations.append('Install advanced antivirus software')
    elif breach_type == 'Insider':
        recommendations.append('Implement access controls and monitoring')
    elif breach_type == 'Physical':
        recommendations.append('Enhance physical security measures')
    
    return recommendations

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'ML Prediction Service'})


@app.route('/api/tfpredict', methods=['POST'])
def tf_predict():
    try:
        data = request.json
        org = data.get('organization')
        breach_type = data.get('breachType')
        year = int(data.get('year', datetime.now().year))

        if not org or not breach_type:
            return jsonify({'error': 'Missing organization or breachType'}), 400

        if org not in industry_encoder.classes_:
            industry_encoder.classes_ = np.append(industry_encoder.classes_, org)
        if breach_type not in type_encoder.classes_:
            type_encoder.classes_ = np.append(type_encoder.classes_, breach_type)

        org_encoded = industry_encoder.transform([org])[0]
        type_encoded = type_encoder.transform([breach_type])[0]

        X = np.array([[org_encoded, type_encoded, year]])
        X[:, 2:] = tf_scaler.transform(X[:, 2:])  

        y_pred_log = tf_model.predict(X, verbose=0)[0][0]
        predicted = int(np.expm1(y_pred_log))

        return jsonify({'predictedRecords': predicted})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Predict breach risk endpoint"""
    try:
        data = request.get_json()
        organization = data.get('organization')
        breach_type = data.get('breachType')
        year = data.get('year', datetime.now().year)
        
        if not organization or not breach_type:
            return jsonify({'error': 'Missing required parameters'}), 400
        
        prediction = predict_breach_risk(organization, breach_type, year)
        
        if prediction is None:
            return jsonify({'error': 'Model not available'}), 500
        
        return jsonify(prediction)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/train', methods=['POST'])
def retrain_model():
    """Retrain the model endpoint"""
    try:
        train_model()
        return jsonify({'message': 'Model retrained successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    load_or_train_model()
    load_tf_model()

    port = int(os.getenv('ML_PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True) 