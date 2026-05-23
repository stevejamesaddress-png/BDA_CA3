# =====================================================
# File: app.py
# Author: Steven James L00196960
#
# Simpple Flask web application 
# to serve real-time flower inferance 
# =====================================================
from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import os
import logging
import time

logging.Formatter.converter = time.gmtime

# Logger in zulu format
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)sZ - API_NODE - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration 
model_dir = os.environ['MODEL_DIR']
model_path = os.path.join(model_dir, 'local_model.pkl')
service_port = int(os.environ['API_PORT'])

logger.info(f"Loading model payload from {model_path}...")
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    logger.info("Model loaded successfully. REST API is armed.")
except Exception as e:
    logger.error(f"Failed to load model. Ensure train.py has run successfully. Error: {e}")
    raise

FLOWER_CLASSES = ['Setosa', 'Versicolor', 'Virginica']


#REST API endpoints 
@app.route('/', methods=['GET'])
def home():
    logger.info("Endpoint Root invoked.")
    return render_template('index.html'), 200

@app.route('/predict', methods=['GET'])
def predict():
    try:
        #get the querry values from HTTP request
        sepal_length = float(request.args.get('sepal_length'))
        sepal_width = float(request.args.get('sepal_width'))
        petal_length = float(request.args.get('petal_length'))
        petal_width = float(request.args.get('petal_width'))
    except (TypeError, ValueError):
        logger.error("Bad Request: Missing or invalid parameters.")
        return jsonify({"status": "error", "Error:": "Please provide valid numerical values."}), 400

    logger.info(f"Inference input SL={sepal_length}, SW={sepal_width}, PL={petal_length}, PW={petal_width}")
    
    input_data = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
    
    # extract prediction
    prediction = model.predict(input_data)[0]
    
    # Extract confidence score 
    # which is the probability of the predicted class
    probabilities = model.predict_proba(input_data)[0]
    confidence = max(probabilities) * 100
    
    #robustness check  
    flower_name = FLOWER_CLASSES[prediction]
    logger.info(f"Prediction result = {flower_name} with {confidence:.2f}% confidence")
    
    return jsonify({
        "status": "success",
        "measurements_received": {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        },
        "predicted_flower": flower_name,
        "confidence_score": round(confidence, 2)
    }), 200

if __name__ == '__main__':
    logger.info(f"Binding FLASK API to 0.0.0.0 on port {service_port}...")
    app.run(host='0.0.0.0', port=service_port)