# /usr/bin/env python3

# toWebMerc: function to convert from GPS coordinates to Mercator coordinates using pyproj
#
# pyproj is a Python interface to PROJ (cartographic projections and coordinate transformations library).
# pyproj Documentation: https://pyproj4.github.io/pyproj/stable/#

from pyproj import Proj, transform
import warnings

# ignore FutureWarning and DeprecationWarning messages for pyproj
[warnings.filterwarnings("ignore", category=alert)
 for alert in [FutureWarning, DeprecationWarning]]

# coordinate transformation
inProj = Proj(init='epsg:4326')
outProj = Proj(init='epsg:3857')


def toWebMerc(long, lat):
    xwm, ywm = transform(inProj, outProj, long, lat)
    return (xwm, ywm)
