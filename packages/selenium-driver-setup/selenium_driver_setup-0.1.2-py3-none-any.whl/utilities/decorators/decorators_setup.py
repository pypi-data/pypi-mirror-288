import logging
from functools import wraps

def exception_non_stopper_decorator(default_value=None):
    """Decorator to catch exceptions, log them, and return a default value instead of raising."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Starting {func.__name__}")
            try:
                result = func(*args, **kwargs)
                logging.info(f"Completed {func.__name__} successfully")
                return result
            except Exception as e:
                logging.error(f"Error in {func.__name__}", exc_info=True)
                return default_value
        return wrapper
    return decorator

def exception_stopper_decorator(func):
    """Decorator to catch exceptions, log them, and re-raise them after logging."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"Completed {func.__name__} successfully")
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}", exc_info=True)
            raise
    return wrapper