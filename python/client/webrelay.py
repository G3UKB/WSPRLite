#!/usr/bin/env python
#
# webrelay.py
#
# Toggle a relay in any relay system that uses webrelay
# 
# Copyright (C) 2019 by G3UKB Bob Cowdery
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
from main.imports import *

#-------------------------------------------------
# This uses the webrelay_min.py Cherrypy server.
# Its only function is to set/reset relays.
# For the full interface use webrelay.py and a browser client.
# Note sequencer uses 1-n but lower level uses 0-(n-1)
def set_web_relay(ip, port, relay, state):
    urllib.request.urlopen('http://%s:%d/set_relay?relay=%d;state=%s' % (ip, port, relay-1, state))
    