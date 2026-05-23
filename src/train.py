import os
import argparse
import logging
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from dotenv import load_dotenv
import mlflow

# Set up logging for the training programme
logging.basicConfig(level=logging.INFO, format='%(asctime)s - TRAIN - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Model Training Programme")
    parser.add_argument('--env-file', type=str, required=False, help="Path to .env file")
    parser.add_argument('--quick', action='store_true', help="Run a quick test without MLflow")
    parser.add_argument('--no-mlflow', action='store_true', help="Disable MLflow tracking")
    args = parser.parse_args()

    # Load environment variables if explicitly provided (e.g. during local tests)
    if args.env_file:
        load_dotenv(args.env_file)
        logger.info(f"Loaded environment variables from {args.env_file}")

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

    # Standard preprocessing for Iris dataset
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

    if args.quick or args.no_mlflow:
        logger.info(f"Quick mode accuracy: {acc:.2f}, F1: {f1:.2f}")
    else:
        logger.info("Logging metrics to MLflow...")
        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(model, "model")

    # Save the model artefact using native pickle
    os.makedirs(model_dir, exist_ok=True)
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    logger.info(f"Model successfully saved to {model_path}")

if __name__ == '__main__':
    logger.info("Starting training pipeline...")
    main()