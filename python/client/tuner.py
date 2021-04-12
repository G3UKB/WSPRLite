#!/usr/bin/env python
#
# tuner.py
#
# Set tuner to the given band
# 
# Copyright (C) 2021 by G3UKB Bob Cowdery
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

# All imports
from imports import *

#-------------------------------------------------
# Band to channel number
band_lookup = {
    160 : 0,
    80 : 1,
    40 : 2,
    20 : 4,
    15 : 6,
    10 : 8
}

#-------------------------------------------------
# Set the tuner for the given band
def set_tuner(tuner, band):
    index = band_lookup[band]
    tuner.set_memory(index)
    