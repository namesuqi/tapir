import inspect
import sys
from lib.common.decorator import *


@func_doc
def test_func():
    """
    test doc
    """
    # print self.__doc__
    pass

if __name__ == "__main__":
    test_func()
    print "end"