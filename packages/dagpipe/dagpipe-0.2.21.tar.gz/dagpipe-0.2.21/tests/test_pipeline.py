import unittest
import dagpipe


@dagpipe.task()
def do_nothing(x):
    """does nothing"""
    return x


@dagpipe.task()
def add_1(x):
    """adds 1 to the input"""
    return x + 1


@dagpipe.task()
def zip_inputs(x, y):
    """zips inputs together"""
    return x, y


@dagpipe.task()
def split_to_two(x):
    """splits into two"""
    return x[0], x[1]


@dagpipe.task()
def append_a(x):
    """appends a to the input"""
    return [x, 'a']

@dagpipe.task()
def append_b(x):
    """appends b to the input"""
    return [x, 'b']
 
@dagpipe.task()
def append_c(x):
    """appends c to the input"""
    return [x, 'c']

@dagpipe.task()
def append_d(x):
    """appends d to the input"""
    return [x, 'd']

@dagpipe.task()
def append_e(x):
    """appends e to the input"""
    return [x, 'e']


class PipelningTest(unittest.TestCase):
    def setUp(self) -> None:
