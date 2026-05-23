# =====================================================
# File: train.py
# Author: Steven James L00196960
# Overview: simple model trained using the iris dataset 
#
# update: removed all options to simplify and 
# removed the MLflow code and git baseline code running fisrt 
# =====================================================
import os
import logging
import pickle
import pandas as pd
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from dotenv import load_dotenv


# Set up logging for the training programme
# we use UTC in zulu format
logging.Formatter.converter = time.gmtime
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)sZ - TRAIN - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%S'
)
logger = logging.getLogger(__name__)

def main():
    # Load environment variables from .env
    load_dotenv()

    data_dir = os.getenv('DATA_DIR')
    data_filename = os.getenv('DATA_FILENAME')
    model_dir = os.getenv('MODEL_DIR')

    if not all([data_dir, data_filename, model_dir]):
        logger.error("Missing required environment variables. Please check your configuration.")
        return

    data_path = os.path.join(data_dir, data_filename)
    model_path = os.path.join(model_dir, 'local_model.pkl')

    logger.info(f"Loading data from {data_path}...")
    try:
        df = pd.read_csv(data_path)
    except FileNotFoundError:
        logger.error(f"Data file not found at {data_path}")
        return

    # prepar ethe data for trining using the features and target below
    X = df.drop(columns=['species', 'Id', 'target'], errors='ignore')
    # Automatically detect the target column name
    if 'target' in df.columns:
        y = df['target']
    elif 'species' in df.columns:
         y = df['species']
    else:
        y = df.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    logger.info("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions, average='macro')

    logger.info(f"Training finished - Accuracy: {acc:.2f}, F1: {f1:.2f}")
  

    # Save the model artefact using native pickle
    os.makedirs(model_dir, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info(f"Model successfully saved to {model_path}")

if __name__ == '__main__':
    logger.info("Starting training pipeline...")
    main()