import time


def timing(func, name, storage):
    def func_wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        storage.append((name, (end-start)*1000))
        return ret
    return func_wrapper