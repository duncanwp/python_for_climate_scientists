
def stack_data_list(data_list, var_name=None, units=None):
    """
    Stacks a list of Ungridded data objects with the same data variable, but different coordinates into a single
    UngriddedData object, with accompanying lat, lon and time data.


    It assumes the coordinates have the same *sets* of coordinates, but that the coordinates themselves are different.

    :param data_list: list of UngriddedData objects to be merged (stacked vertically)
    :param string var_name: Name of final data variable
    :param string units: Units of final data variable
    :return: A merged UngriddedData object
    """
    import numpy as np
    from cis.data_io.ungridded_data import UngriddedData, Metadata
    from cis.data_io.Coord import Coord

    coords = []
    all_data = np.hstack((d.data_flattened for d in data_list))

    # Create mask (not all datasets might be masked)
    mask = np.hstack((d.data.mask.ravel() if isinstance(d.data, np.ma.MaskedArray) else np.zeros(d.shape, np.bool) for d in data_list))
    all_data = np.ma.MaskedArray(all_data, mask)

    for c in data_list[0].coords():
        coord_data = np.hstack((d.coord(c).data_flattened for d in data_list))
        coords.append(Coord(coord_data, c.metadata, axis=c.axis))

    return UngriddedData(all_data,
                         Metadata(name=var_name or data_list[0].name(), units=units or data_list[0].units),
                         coords)
