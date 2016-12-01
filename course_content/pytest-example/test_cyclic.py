"""
Test the add_cyclic_point function from the cyclic module.

In this module we'll write simple functions to test the code we wrote
for add_cyclic_point in the cyclic module. We'll be using pytest to
run the tests, and for some helpful features when writing tests.

"""
import numpy as np

from cyclic import add_cyclic_point


def test_default():
    data = np.array([0, 1, 2, 3, 4], dtype=np.int)
    cyclic_data = add_cyclic_point(data)
    assert cyclic_data.size == data.size + 1
    assert cyclic_data[0] == cyclic_data[-1]
    assert (cyclic_data[:-1] == data).all()
