#!/usr/bin/env python3
#
# defs.py
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

# Global definitions for WSPRLite application

# UI idle callbacks 200ms
IDLE_TICKER = 200   

# Server connection info
RQST_IP = '0.0.0.0'
RQST_PORT = 10001

# RPiWebRelay address for LPF selection 
WEBRELAY_IP = '192.168.1.115'
WEBRELAY_PORT = 8080
BANDS_AVAILABLE = ('160','80','40','20','15','10')

# Client connection info
SERVER_IP = '192.168.1.114'
SERVER_PORT = 10001

# Timer commands
WAIT_START = 0
WAIT_STOP = 1
# Timer status
IDLE = 'IDLE'
WAIT_START = 'WAIT-START'
TX_CYCLING = 'TX-CYCLING'
WAIT_STOP = 'WAIT-STOP'

# Request types
GET_CALLSIGN = 'get-callsign'
GET_LOCATOR = 'get-locator'
GET_FREQ = 'get-freq'
SET_FREQ = 'set-freq'
SET_BAND = 'set-band'
SET_TX = 'set-tx'
SET_IDLE = 'set-idle'
GET_STATUS = 'get-status'
