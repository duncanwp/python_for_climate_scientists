import cis
import numpy as np


def subset_region(ungridded_data):
    from cartopy.io.shapereader import Reader, natural_earth
    from shapely.geometry import MultiPoint, box
    from shapely.ops import unary_union
    from cis.utils import fix_longitude_range

    northern_africa = box(-20, 0, 50, 40)
    southern_africa = box(10, -40, 50, 0)
    combined_africa = unary_union([northern_africa, southern_africa])

    # It would be nice to make use of the asMultiPoint interface but it's not working for z-points at the moment
    # cis_data = np.vstack([sim_points.lon.data, sim_points.lat.data, np.arange(len(sim_points.lat.data))])
    # points = MultiPoint(cis_data.T)
    # OR:
    # geos_data = asMultiPoint(cis_data.T)

    # Create shapely Points, we use the z coord as a cheat for holding an index to our original points
    points = MultiPoint([(lon, lat, i)
                         for i, (lat, lon) in enumerate(zip(ungridded_data.lat.points, ungridded_data.lon.points))])

    # Perform the actual calculation
    selection = combined_africa.intersection(points)

    # Pull out the indices
    indices = np.asarray(selection).T[2].astype(np.int)
    return ungridded_data[indices]