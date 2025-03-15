import os
import subprocess
import logging

# Ensure logging directory exists
log_dir = "./logging"
os.makedirs(log_dir, exist_ok=True)

# Configure logging
log_file = os.path.join(log_dir, "pipeline.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def run_script(script_name):
    """Runs a Python script and logs the output."""
    try:
        logging.info(f"Starting execution of {script_name}.")
        result = subprocess.run(["python", script_name], capture_output=True, text=True, check=True)
        logging.info(f"Execution of {script_name} completed successfully.")
        logging.info(f"Output:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error while executing {script_name}: {e.stderr}", exc_info=True)
        raise

if __name__ == "__main__":
    logging.info("Pipeline execution started.")

    try:
        # Step 1: Run the ETL process
        print("Running step 1: etl.py")
        run_script("etl.py")
        print("Sucessfully ran step 1: etl.py")
        # Step 2: Run the model training process
        print("Running step 2: model_training.py")
        run_script("model_training.py")
        print("Sucessfully ran step 2: model_training.py")

        logging.info("Master Pipeline execution completed successfully.")

    except Exception as e:
        logging.critical("Pipeline execution failed.", exc_info=True)

    print("Master Pipeline execution completed. Check logs for details.")
