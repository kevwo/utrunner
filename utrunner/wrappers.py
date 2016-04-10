import time
import pdb
import traceback
import sys


def timing(func, name, storage):
    def func_wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        storage.append((name, (end-start)*1000))
        return ret
    return func_wrapper


def debug_testcase(testcase):
    """
    To be used for converting unittest.TestCase.run into unittest.TestCase.debug() function that will ignore any params
     instead of raising an exception
    :param testcase: The TestCase object to modify
    :return: Nothing
    """
    def debug_func(*args, **kwargs):
        try:
            ret = testcase.debug()
            return ret
        except:
            _, _, tb = sys.exc_info()
            traceback.print_exc()
            pdb.post_mortem(tb)
            raise
    testcase.run = debug_func