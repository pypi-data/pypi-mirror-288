def kminlen(min_len_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) < min_len_value:
                raise ValueError(
                    f"Composite type length should not be below {min_len_value}"
                )
            return func(*args, **kwargs)

        return wrapper

    return decorator
