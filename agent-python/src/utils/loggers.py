# src/utils/logger.py

import logging

def get_logger(name):
    """
    Configure and return a basic logger.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(name)

# An example
if __name__ == "__main__":
    logger = get_logger("test_logger")
    logger.info("This is an INFO message.")
    logger.error("This is an ERROR message.")