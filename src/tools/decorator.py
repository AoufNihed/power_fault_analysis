def log_execution(func):
    """Decorator to log execution of functions."""
    def wrapper(*args, **kwargs):
        print(f"⚙️ Executing {func.__name__}...")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__} execution completed.")
        return result
    return wrapper
