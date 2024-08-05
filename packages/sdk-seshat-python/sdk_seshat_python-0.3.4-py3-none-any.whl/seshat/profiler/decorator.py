def track(func):
    from seshat.profiler.base import profiler

    def wrapper(*args, **kwargs):
        return profiler.run(func, *args, **kwargs)

    return wrapper
