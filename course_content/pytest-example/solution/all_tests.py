"""
All the test functions for the pytest example in the order they should
be presented in.

#1 is in the default test file (passes)
#2 generates a failure, it will be replaced with #3 (fails)
#3 replaces #2 (passes)
#4 is added to cover the specified axis case (passes)
#5 demonstrates a problem with masked arrays (fails) [optional]

"""

# 1
def test_default():
    data = np.array([0, 1, 2, 3, 4], dtype=np.int)
    cyclic_data = add_cyclic_point(data)
    assert cyclic_data.size == data.size + 1
    assert cyclic_data[0] == cyclic_data[-1]
    assert (cyclic_data[:-1] == data).all()


# 2
def test_specified_axis():
    data = np.array([0, 1, 2, 3, 4], dtype=np.int)
    cyclic_data = add_cyclic_point(data, axis=1)
    assert cyclic_data.size == data.size + 1
    assert cyclic_data[0] == cyclic_data[-1]
    assert (cyclic_data[:-1] == data).all()


# 3
def test_invalid_axis():
    data = np.array([0, 1, 2, 3, 4], dtype=np.int)
    with pytest.raises(ValueError):
        cyclic_data = add_cyclic_point(data, axis=1)

# 4
def test_specified_axis():
    data = np.ones([5, 6], dtype=np.int) * np.arange(6, dtype=np.int)
    cyclic_data = add_cyclic_point(data, axis=0)
    original_rows, original_cols = data.shape
    assert cyclic_data.shape == (original_rows + 1, original_cols)
    assert (cyclic_data[0, :] == cyclic_data[-1, :]).all()
    assert (cyclic_data[:-1] == data).all()


# 5 (optional, if there is time left)
def test_masked_input():
    data = ma.array([0, 1, 999, 3, 4], mask=[0, 0, 1, 0, 0], dtype=np.int)
    cyclic_data = add_cyclic_point(data)
    assert ma.is_masked(cyclic_data)
