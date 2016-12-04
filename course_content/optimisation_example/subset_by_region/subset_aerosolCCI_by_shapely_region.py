import cis
import numpy as np

files = ["../../resources/WorkshopData2016/AerosolCCI/20080411002335-ESACCI-L2P_AEROSOL-AER_PRODUCTS-AATSR-ENVISAT-ORAC_31962-fv03.04.nc",
         "../../resources/WorkshopData2016/AerosolCCI/20080411020411-ESACCI-L2P_AEROSOL-AER_PRODUCTS-AATSR-ENVISAT-ORAC_31963-fv03.04.nc",
         "../../resources/WorkshopData2016/AerosolCCI/20080411034447-ESACCI-L2P_AEROSOL-AER_PRODUCTS-AATSR-ENVISAT-ORAC_31964-fv03.04.nc",
         "../../resources/WorkshopData2016/AerosolCCI/20080411052523-ESACCI-L2P_AEROSOL-AER_PRODUCTS-AATSR-ENVISAT-ORAC_31965-fv03.04.nc",
         "../../resources/WorkshopData2016/AerosolCCI/20080411070559-ESACCI-L2P_AEROSOL-AER_PRODUCTS-AATSR-ENVISAT-ORAC_31966-fv03.04.nc"]


def subset_region(ungridded_data, region):
    from shapely.geometry import MultiPoint

    cis_data = np.vstack([ungridded_data.lon.data, ungridded_data.lat.data, np.arange(len(ungridded_data.lat.data))])
    points = MultiPoint(cis_data.T.tolist())

    # Perform the actual calculation
    selection = region.intersection(points)

    # Pull out the indices
    if selection.is_empty:
        indices = []
    else:
        indices = np.asarray(selection).T[2].astype(np.int)

    return ungridded_data[indices]


def make_africa_box():
    from shapely.geometry import box
    from shapely.ops import unary_union

    northern_africa = box(-20, 0, 50, 40)
    southern_africa = box(10, -40, 50, 0)
    combined_africa = unary_union([northern_africa, southern_africa])

    return combined_africa


def make_african_land():
    from cartopy.io.shapereader import Reader, natural_earth
    from shapely.ops import unary_union

    shpfile = Reader(natural_earth(resolution='110m', category='cultural', name='admin_0_countries'))

    filtered_records = shpfile.records()
    filtered_records = filter(lambda x: x.attributes['continent'] == 'Africa', filtered_records)

    region_poly = unary_union([r.geometry for r in filtered_records])

    return region_poly


def read_and_subset_data(filename):
    d = cis.read_data(filename, "AOD550")
    return subset_region(d, make_african_land())


def subset_aerosol_cci_over_africa():
    from subset_by_region.utils import stack_data_list
    import multiprocessing
    pool = multiprocessing.Pool()
    subsetted_data = pool.map(read_and_subset_data, files)
    subset = stack_data_list(subsetted_data)
    return subset


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    subset = subset_aerosol_cci_over_africa()
    subset.plot(xaxis='longitude', yaxis='latitude')
    plt.show()
