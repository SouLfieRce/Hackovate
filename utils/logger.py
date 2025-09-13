import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str = "app", log_file: str = "app.log") -> logging.Logger:
    """
    Returns a logger instance with both console and file handlers.
    
    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        ch.setFormatter(ch_formatter)

        # File handler (rotating)
        fh = RotatingFileHandler(log_file, maxBytes=5_000_000, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        fh.setFormatter(fh_formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger

# Example usage:
if __name__ == "__main__":
    log = get_logger("demo")
    log.info("Logger is working!")
    log.error("This is an error example.")
