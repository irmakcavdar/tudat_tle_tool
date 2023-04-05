#TLE TEST in TUDAT:

import math
import numpy as np
import pandas as pd
# from sgp4.api import Satrec, jday
from numpy import linalg as LA
from matplotlib import pyplot as plt
from math import modf
# from satellite_tle import fetch_tle_from_celestrak #this is used to fetch the TLE directly in python
import csv
from datetime import datetime, timedelta
from astropy.time import Time

#Tudat imports:
from tudatpy.kernel.interface import spice
from tudatpy.kernel.astro import element_conversion
from tudatpy.kernel import constants

# norad_id = input("Enter the desired norad id:", )
# Here the user can provide any desired input and the latest TLE of the provided satellite will be downloaded
norad_catalogue_number = 19688

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve
urlretrieve('https://celestrak.org/NORAD/elements/gp.php?CATNR='+ str(norad_catalogue_number), 'tle_data_' + str(norad_catalogue_number) + ".dat")

tle = []

file_name = 'tle_data_' + str(norad_catalogue_number) + ".dat"

with open(file_name, 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    tle.append(row)

#These are the line 1 and line 2 of the TLE, they are named s and t to be compatible with the inputs of SGP4 tool from astropy
s = tle[1][0]
t = tle[2][0]

#Part 2: Calculate the desired time in seconds since J2000
j2000_time = Time("2000-01-01 12:00:00.000", format='iso', scale='utc')

jd, fr = jday(2023, 4, 1, 10, 0, 0)
jd_begin = jd + fr
t = Time(jd_begin, format='jd', scale='utc')

utc = datetime.strptime(t.iso, '%Y-%m-%d %H:%M:%S.%f')
time_difference = utc - j2000_time.datetime
seconds = time_difference.total_seconds()

epoch = seconds

# state = spice.get_cartesian_state_from_tle_at_epoch(epoch, "...")
