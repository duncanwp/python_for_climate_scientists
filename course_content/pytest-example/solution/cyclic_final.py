"""Adding a cyclic points to arrays."""
import numpy.ma as ma


def add_cyclic_point(data, axis=-1):
    """
    Add a cyclic point to an array.

    Args:

    * data:
        An n-dimensional array of data to add a cyclic point to.

    Kwargs:

    * axis:
        Specifies the axis of the data array to add the cyclic point to.
        Defaults to the right-most axis.

    Returns:

    * cyclic_data:
        The data array with a cyclic point added.

    Examples:

    Adding a cyclic point to a data array, where the cyclic dimension is
    the right-most dimension

    >>> import numpy as np
    >>> data = np.ones([5, 6]) * np.arange(6)
    >>> cyclic_data = add_cyclic_point(data)
    >>> print(cyclic_data)
    [[ 0.  1.  2.  3.  4.  5.  0.]
     [ 0.  1.  2.  3.  4.  5.  0.]
     [ 0.  1.  2.  3.  4.  5.  0.]
     [ 0.  1.  2.  3.  4.  5.  0.]
     [ 0.  1.  2.  3.  4.  5.  0.]]

    """
    slicer = [slice(None)] * data.ndim
    try:
        slicer[axis] = slice(0, 1)
    except IndexError:
        raise ValueError('specified axis does not exist in the input')
    new_data = ma.concatenate((data, data[slicer]), axis=axis)
    return new_data
