import timeit

def timed_execution(func):
    def wrapper(*args, **kwargs):
        start_time = timeit.default_timer()
        result = func(*args, **kwargs)
        end_time = timeit.default_timer()
        execution_time = end_time - start_time
        print(f"Execution time for {func.__name__}: {execution_time} seconds")
        return result
    
    return wrapper