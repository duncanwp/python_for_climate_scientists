"""
Test the add_cyclic_point function from the cyclic module.

In this module we'll write simple functions to test the code we wrote
for add_cyclic_point in the cyclic module. We'll be using pytest to
run the tests, and for some helpful features when writing tests.

"""
import numpy as np

from cyclic import add_cyclic_point


def test_default():
    """
    Test add_cyclic_point with a 1-d array and no keywords.

    Input: [0, 1, 2, 3, 4]
    Expected ouput: [0, 1, 2, 3, 4, 0]

    """
    data = np.array([0, 1, 2, 3, 4], dtype=np.int)
    cyclic_data = add_cyclic_point(data)
    # The output should be 1 element longer than the input:
    assert cyclic_data.size == data.size + 1
    # The first and last elements of the output should be the same:
    assert cyclic_data[0] == cyclic_data[-1]
    # The elements of the output up-to the last should be the same as
    # the input:
    assert (cyclic_data[:-1] == data).all()
