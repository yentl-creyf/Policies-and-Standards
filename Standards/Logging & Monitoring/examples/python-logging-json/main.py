import logging
import json
import sys
from datetime import datetime, timezone

# Define a custom JSON formatter
class JSONFormatter(logging.Formatter):
    def format(self, record) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "name": record.name,
            "module": record.module,
            "filename": record.filename,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        
        # Include exception details if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_record)

# Configure the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a stream handler to output to stdout
handler = logging.StreamHandler(sys.stdout)

# Attach JSON formatter to the handler
handler.setFormatter(JSONFormatter())

# Add the handler to the logger
logger.addHandler(handler)

if __name__ == "__main__":
    # Example log statements
    logger.debug("This is a debug message for tracing finer details.")
    logger.info("This is an informational message to keep track of events.")
    logger.warning("This is a warning about a potential issue.")
    logger.error("This is an error message indicating something went wrong.")
    
    try:
        # Simulating an exception
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("An exception occurred: Division by zero")

    logger.critical("This is a critical issue requiring immediate attention.")
