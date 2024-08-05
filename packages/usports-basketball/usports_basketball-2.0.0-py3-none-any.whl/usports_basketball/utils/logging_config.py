import logging


def setup_logging():
    """setsup logging configurations"""
    logging.basicConfig(
        level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output logs to the console
        ],
        datefmt="%d/%m/%Y %H:%M:%S",
    )
