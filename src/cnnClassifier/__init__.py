import os # for file path management
import sys # given sys.stdout for output
import logging # for logging messages

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"  # time, log level name, module name, log message
log_dir = "logs" # log directory name is log_dir
log_filepath = os.path.join(log_dir, "running_logs.log") # creates log file inside the log directory
os.makedirs(log_dir, exist_ok=True) # creates the log dir, if it is not present

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,

    handlers=[
        logging.FileHandler(log_filepath), # logs message to the file 
        logging.StreamHandler(sys.stdout) # logs message to the screen
    ]
)

logger = logging.getLogger("cnnClassifierLogger") #Provides a logger object named "cnnClassifierLogger" 
        # that can be used throughout the program to log messages at various levels (INFO, ERROR, etc.).