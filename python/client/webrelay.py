#!/usr/bin/env python
#
# webrelay.py
#
# Set relays for a given band
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

# All imports
from imports import *

#-------------------------------------------------
# Band to channel number
band_lookup = {
    160 : 0,
    80 : 1,
    40 : 2,
    20 : 3,
    15 : 4,
    10 : 5
}

#-------------------------------------------------
# Set the channel for the given band, first resetting all channels
# such that only the target LPF is selected.
def set_lpf(ip, port, band):
    on_ch = band_lookup[band]
    # Turn all channels off first
    for ch in range(6):
        r = set_web_relays(ip, port, ch, 'off')
        if not r[0]:
            return(r)
    # Set the target channel
    r = set_web_relays(ip, port, on_ch, 'on')
    return r

#-------------------------------------------------
# This uses the webrelay_min.py Cherrypy server.
# Its only function is to set/reset relays.
# For the full interface use webrelay.py and a browser client.
# Note that the minimal web relay app requires channels to be zero based
def set_web_relays(ip, port, relay, state):
    try:
        urllib.request.urlopen('http://%s:%d/set_channel?relay=%d;state=%s' % (ip, port, relay, state))
    except Exception as e:
       return (False, str(e))
    return (True, '')
    