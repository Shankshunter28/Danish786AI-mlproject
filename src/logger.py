import logging
import os
from datetime import datetime

# Generate a unique log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Create the "logs" folder in the current working directory (if it doesn't exist)
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

# Define the full log file path
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Configure logging settings
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] [Line:%(lineno)d] %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Optional: Also log to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s"))
logging.getLogger().addHandler(console_handler)

if __name__ == "__main__":
    logging.info("Logging has started successfully.")
    
    logging = logging.getLogger(__name__)

