from functools import wraps
import importlib

def log_func(func):
    import logging
    logging.basicConfig(filename='{}.log'.format(func.__name__), level=logging.INFO)

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(
            'Ran with args: {}, and kwargs: {}'.format(args, kwargs))

        return func(*args, **kwargs)

    return wrapper


def time_func(func):
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time() - t1
        print('{} ran in: {} sec'.format(func.__name__, t2))
        return result

    return wrapper


def class_from_name(module_name, class_name, args):

    # Load the module first, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)

    # Get  the class and create an object, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)(args)

    return c


def get_next_state(items, conditions):
        
    next_state = next((x for x in items if eval(conditions)), None)
    if next_state is None:
        raise "Input not supported for current state"

    return next_state
