import json
import logging
import os
import sys
import time


class CustomLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        frame = sys._getframe(6)  # Adjust this number if needed
        self.filename = os.path.basename(frame.f_code.co_filename)
        self.lineno = frame.f_lineno


def _initialize_logger():
    logger = logging.getLogger(__name__)

    # Clear any existing handlers
    if logger.handlers:
        logger.handlers.clear()

    # Set the logger level
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler('file.log', mode='a', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler for console output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter('%(filename)s:%(lineno)d - %(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Set the custom LogRecord factory
    logging.setLogRecordFactory(CustomLogRecord)

    return logger


logger = _initialize_logger()


def log_(level, records):
    if not isinstance(records, (list, tuple)):
        records = [records]
    for record in records:
        if isinstance(record, dict):
            formatted_record = ', '.join(f"{key}: {value}" for key, value in record.items())
        elif isinstance(record, list):
            formatted_record = ', '.join(map(str, record))
        else:
            formatted_record = str(record)

        if level == 'error':
            logger.error('%s', formatted_record)
        elif level == 'warning':
            logger.warning('%s', formatted_record)
        elif level == 'info':
            logger.info('%s', formatted_record)
        elif level == 'debug':
            logger.debug('%s', formatted_record)
        else:
            logger.info('%s', formatted_record)

        # Flush and sync after each log entry
        for handler in logger.handlers:
            handler.flush()
            if isinstance(handler, logging.FileHandler):
                os.fsync(handler.stream.fileno())

        # Add a small delay to ensure real-time display
        time.sleep(0.01)

    return records

def debug(records):
    return log_('debug', records)

def info(records):
    return log_('info', records)
    
def warning(records):
    return log_('warning', records)

def error(records):
    return log_('error', records)

def json_print(msg):
    if isinstance(msg, dict):
        return json.dumps(msg, indent=2)
    elif isinstance(msg, str):
        try:
            return json.dumps(json.loads(msg), indent=2)
        except json.JSONDecodeError:
            return json.dumps({"message": msg}, indent=2)
    else:
        return json.dumps({"data": str(msg)}, indent=2)
    
    
    