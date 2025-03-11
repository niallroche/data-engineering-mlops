from flask import Flask, request, jsonify, send_from_directory
import joblib
import psycopg2
import json
import os
import time
import numpy as np

app = Flask(__name__, static_folder="../static")

# Load the pre-trained model
model = joblib.load('model/logistic_model.pkl')

# Environment configuration
USE_DATABASE = os.getenv('USE_DATABASE', 'true').lower() == 'true'
IS_DOCKER = os.getenv('IS_DOCKER', 'false').lower() == 'true'

# Database configuration if enabled
if USE_DATABASE:
    DB_CONFIG = {
        'dbname': os.getenv('POSTGRES_DB', 'flask_logs'),
        'user': os.getenv('POSTGRES_USER', 'postgres'),
        'password': os.getenv('POSTGRES_PASSWORD', 'your_password'),
        'host': os.getenv('POSTGRES_HOST', 'db' if IS_DOCKER else 'localhost'),
        'port': os.getenv('POSTGRES_PORT', '5432')
    }

def get_db_connection():
    if USE_DATABASE:
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            conn.autocommit = True
            return conn
        except Exception as e:
            app.logger.error(f"Database connection failed: {str(e)}")
            return None
    return None

@app.route('/predict', methods=['POST'])
def predict():
    start_time = time.time()
    try:
        data = request.get_json(force=True)
        features = data.get("features")
        
        # Get prediction and probability
        prediction = model.predict([features])
        probabilities = model.predict_proba([features])
        confidence = float(np.max(probabilities[0]))  # Get the highest probability
        
        response = {
            "prediction": int(prediction[0]),
            "confidence": confidence
        }
        
        processing_time = time.time() - start_time

        # Log the request and prediction in the database
        if USE_DATABASE:
            conn = get_db_connection()
            if conn:
                try:
                    cur = conn.cursor()
                    insert_query = """
                        INSERT INTO prediction_logs 
                        (input_features, prediction, timestamp, processing_time, confidence) 
                        VALUES (%s, %s, CURRENT_TIMESTAMP, %s, %s)
                    """
                    cur.execute(insert_query, (
                        json.dumps(data), 
                        int(prediction[0]),
                        float(processing_time),
                        confidence
                    ))
                    cur.close()
                    conn.close()
                except Exception as e:
                    app.logger.error(f"Database logging failed: {str(e)}")
                    # Continue even if logging fails
        
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve the static HTML form
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)