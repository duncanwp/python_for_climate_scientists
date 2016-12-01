"""Model input/output tools."""
# (c) Copyright 2016 Andrew Dawson.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import (absolute_import, division, print_function)  #noqa

import os.path

from netCDF4 import Dataset


class NetCDFWriter(object):
    """Write model output to a NetCDF file."""

    def __init__(self, model, filename, overwrite=True):
        """
        Initialize a netCDF output writer object for a given model.

        Arguments:

        * model
            An instance of `heateqn.model.HeatEquationModel` to provide
            output services to.

        * filename
            The name of the NetCDF file to use for output.

        Keyword argument:

        * overwrite
            If `True` the writer will overwrite the specified file if it
            already exists, and if `False` an error will be raised if
            the specified filename already exists. Default is `True`
            (existing file will be overwritten).

        """
        self.model = model
        self.filename = filename
        if not overwrite and os.path.exists(filename):
            msg = ('cannot write output to "{}", the file already '
                   'exists but overwrite=False')
            raise IOError(msg.format(filename))
        # Open a new netCDF dataset:
        self.ds = Dataset(filename, mode='w')
        # Create dimensions for time, latitude and longitude, the time
        # dimension has unlimited size:
        self.ds.createDimension('time')
        self.ds.createDimension('latitude', size=model.nlat)
        self.ds.createDimension('longitude', size=model.nlon)
        # Create coordinate variables for time, latitude and longitude, the
        # values of depth can be set immediately:
        self.time = self.ds.createVariable('time', 'f4', dimensions=['time'])
        time_units = 'seconds since {}'.format(
            model.start_time.strftime('%Y-%m-%d %H:%M:%S'))
        self.time.setncatts({'standard_name': 'time', 'units': time_units})
        latitude = self.ds.createVariable('latitude', 'f4',
                                          dimensions=['latitude'])
        longitude = self.ds.createVariable('longitude', 'f4',
                                           dimensions=['longitude'])
        latitude.setncatts({'standard_name': 'latitude',
                            'units': 'degrees_north'})
        longitude.setncatts({'standard_name': 'longitude',
                             'units': 'degrees_east'})
        latitude[:], longitude[:] = self.model.engine.grid_latlon()
        lat_lon = self.ds.createVariable('latitude_longitude', 'i4')
        lat_lon.setncatts({'grid_mapping_name': 'latitude_longitude',
                           'longitude_of_prime_meridian': 0.,
	                       'semi_major_axis': 6371229.,
		                   'semi_minor_axis': 6371229.})
        # Create variables to hold the model state:
        self.u = self.ds.createVariable(
            'uwnd',
            'f4',
            dimensions=['time', 'latitude', 'longitude'],
            zlib=True)
        self.v = self.ds.createVariable(
            'vwnd',
            'f4',
            dimensions=['time', 'latitude', 'longitude'],
            zlib=True)
        self.vrt = self.ds.createVariable(
            'vrt',
            'f4',
            dimensions=['time', 'latitude', 'longitude'],
            zlib=True)
        self.u.setncatts({'standard_name': 'eastward_wind',
                          'units': 'm s-1',
                          'grid_mapping': 'latitude_longitude'})
        self.v.setncatts({'standard_name': 'northward_wind',
                          'units': 'm s-1',
                          'grid_mapping': 'latitude_longitude'})
        self.vrt.setncatts({'standard_name': 'atmosphere_relative_vorticity',
                            'units': 's-1',
                            'grid_mapping': 'latitude_longitude'})

    def save(self):
        """Save the current model state to the output netCDF file."""
        if not self.ds.isopen():
            msg = 'cannot save output: the NetCDF writer is already closed'
            raise IOError(msg)
        index = self.time.size
        self.time[index] = self.model.t
        self.u[index] = self.model.u_grid
        self.v[index] = self.model.v_grid
        self.vrt[index] = self.model.vrt_grid

    def flush(self):
        """
        Write the output file to disk.

        The netCDF file may be buffered. Whilst calling `save` will
        append a record to the output, it may not be written to disk
        immediately.

        """
        if self.ds.isopen():
            self.ds.sync()

    def close(self):
        """Close the netCDF output file."""
        if self.ds.isopen():
            self.ds.close()
