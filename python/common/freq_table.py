#!/usr/bin/env python3
#
# freq_table.py
# 
# Copyright (C) 2020 by G3UKB Bob Cowdery
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#    
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#    
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    
#  The author can be reached by email at:   
#     bob@bobcowdery.plus.com
#

import random

#------------------------------------------------------------
# Allocated WSPR bands
band_lookup = {
    160: (1.836600, 1.838100),
    80: (3.568600, 3.570100),
    60: (5.364700, 5.366200),
    40: (7.038600, 7.040100),
    30: (10.138700, 10.140200),
    20: (14.095600, 14.097100),
    17: (18.104600, 18.106100),
    15: (21.094600, 21.096100),
    12: (24.924600, 24.926100),
    10: (28.124600, 28.126100),
    6: (50.293000, 50.294500),
    4: (70.091000, 70.092500),    
    2: (144.489000, 144.490500)
}

#------------------------------------------------------------
# Return a random TX frequency within the given band.
def get_tx_freq(band):
    range = band_lookup[band]
    return round(random.uniform(range[0], range[1]), 6)

#------------------------------------------------------------
# Given a frequency find the band it falls inside
def find_band(freq):
    for band in band_lookup.keys():
        lower = band_lookup[band][0]
        upper = band_lookup[band][1]
        if freq >= lower and freq <= upper:
            # Success
            return lower, upper, band
    # Failed!
    return None

#------------------------------------------------------------
# String copy of band limits.
def get_band_limits():
    return '''
160: (1.836600, 1.838100),
80:  (3.568600, 3.570100),
60:  (5.364700, 5.366200),
40:  (7.038600, 7.040100),
30:  (10.138700, 10.140200),
20:  (14.095600, 14.097100),
17:  (18.104600, 18.106100),
15:  (21.094600, 21.096100),
12:  (24.924600, 24.926100),
10:  (28.124600, 28.126100),
6:   (50.293000, 50.294500),
4:   (70.091000, 70.092500),    
2:   (144.489000, 144.490500)
'''
    