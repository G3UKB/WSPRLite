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
    160: (1.838000, 1.838200),
    80: (3.594000, 3.594200),
    60: (5.288600, 5.288800),
    40: (7.040000, 7.040200),
    30: (10.140100, 10.140300),
    20: (14.097000, 14.097200),
    17: (18.106000, 18.106200),
    15: (21.096000, 21.096200),
    12: (24.926000, 24.926200),
    10: (28.126000, 28.126200),
    6: (50.294400, 50.294600),    
    2: (144.489900, 144.490100)
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
160: (1.838000, 1.838200)
80: (3.594000, 3.594200)
60: (5.288600, 5.288800)
40: (7.040000, 7.040200)
30: (10.140100, 10.140300)
20: (14.097000, 14.097200)
17: (18.106000, 18.106200)
15: (21.096000, 21.096200)
12: (24.926000, 24.926200)
10: (28.126000, 28.126200)
6: (50.294400, 50.294600)   
2: (144.489900, 144.490100)
'''
    