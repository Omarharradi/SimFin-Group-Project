import pandas as pd
import numpy as np
import xgboost as xgb
import argparse
import joblib
import os
import logging
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils.class_weight import compute_class_weight

# Ensure the required directories exist
log_dir = "./logging"
output_dir = "./output"
os.makedirs(log_dir, exist_ok=True)  # Ensure logging directory exists
os.makedirs(output_dir, exist_ok=True)  # Ensure output directory exists

# Configure logging
log_file = os.path.join(log_dir, "model_training.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def load_data(csv_file):
    """Load and preprocess data from a CSV file."""
    logging.info(f"Loading data from {csv_file}.")
    
    try:
        df = pd.read_csv(csv_file)
        logging.info(f"Data loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")

        # Ensure necessary columns exist
        required_columns = {'Date', 'Close_Ticker_Shifted', 'Target', 'Ticker'}
        if not required_columns.issubset(df.columns):
            error_msg = f"CSV file must contain the following columns: {required_columns}"
            logging.error(error_msg)
            raise ValueError(error_msg)

        # Define features and target
        features = df.drop(columns=['Date', 'Close_Ticker_Shifted', 'Target', 'Ticker'])
        target = df['Target']
        
        logging.info("Feature and target variables prepared successfully.")
        return features, target

    except Exception as e:
        logging.error(f"Error loading data: {e}", exc_info=True)
        raise

def train_xgb(features, target):
    """Train an XGBoost model and evaluate performance."""
    logging.info("Starting XGBoost training.")

    try:
        # Compute class weights for imbalance handling
        class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(target), y=target)
        scale_pos_weight = class_weights[1] / class_weights[0]
        logging.info(f"Computed class weights: {class_weights}.")

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42, stratify=target
        )
        logging.info(f"Data split into training ({X_train.shape[0]} samples) and testing ({X_test.shape[0]} samples).")

        # Convert data into DMatrix format
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)

        # XGBoost parameters
        params = {
            "objective": "binary:logistic",
            "eval_metric": "logloss",
            "eta": 0.01,
            "max_depth": 8,
            "subsample": 0.9,
            "colsample_bytree": 0.8,
            "gamma": 5.0,
            "alpha": 1.0,
            "lambda": 7.0,
            "random_state": 42
        }
        logging.info("XGBoost parameters set.")

        # Train the model with early stopping
        evallist = [(dtrain, "train"), (dtest, "eval")]
        num_rounds = 500
        logging.info("Starting model training with early stopping.")
        model = xgb.train(params, dtrain, num_rounds, evals=evallist, early_stopping_rounds=20, verbose_eval=50)
        logging.info("Model training completed.")

        # Predict on test data
        y_pred_prob = model.predict(dtest)
        y_pred = (y_pred_prob > 0.5).astype(int)
        
        # Evaluate performance
        accuracy = accuracy_score(y_test, y_pred)
        logging.info(f"Model Accuracy (Test): {accuracy:.4f}")
        logging.info(f"Classification Report (Test):\n{classification_report(y_test, y_pred)}")

        # Predict on train data
        y_pred_t = model.predict(dtrain)
        y_pred_t = (y_pred_t > 0.5).astype(int)
        accuracy_train = accuracy_score(y_train, y_pred_t)
        logging.info(f"Model Accuracy (Train): {accuracy_train:.4f}")

        # Save the model in the output directory
        model_path = os.path.join(output_dir, "xgb.joblib")
        joblib.dump(model, model_path)
        logging.info(f"Model saved at {model_path}.")

    except Exception as e:
        logging.error(f"Error during model training: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    logging.info("Script execution started.")

    try:
        csv_file = os.path.join(output_dir, "processed_stock_data.csv")  # Use processed data from ETL script
        features, target = load_data(csv_file)
        train_xgb(features, target)

        logging.info("Model training completed successfully.")

    except Exception as e:
        logging.critical("Script execution failed.", exc_info=True)
    
    print(f"Model training completed successfully. Model saved at {os.path.join(output_dir, 'xgb.joblib')}.")
