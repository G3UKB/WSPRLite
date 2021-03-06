#!/usr/bin/env python3
#
# netif.py
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

# Python imports
import os, sys
import threading
import socket
import pickle

# Application imports
from common.defs import *

"""
Interface to the WSPRLite client application:

Commands are UDP:
    
"""

#========================================================================
# Net interface
class NetIF(threading.Thread):
    
    #----------------------------------------------
    # Constructor
    def __init__(self, callback):
        """
        Constructor
        
        Arguments:
            callback    --  callback here when data arrives
            
        """

        super(NetIF, self).__init__()
        self.__callback = callback
        
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.bind((RQST_IP, RQST_PORT))
        self.__sock.settimeout(3)
        
        self.__address = None
        self.__terminate = False
    
    #----------------------------------------------
    # Terminate
    def terminate(self):
        """ Terminate thread """
        
        self.__terminate = True
    
    #----------------------------------------------
    # Do response
    def response(self, data):
        """
        Send response data
        
        Arguments:
            data    --  bytestream to send
        
        """
        
        if self.__address != None:
            try:
                pickledData = pickle.dumps(data)
                self.__sock.sendto(pickledData, self.__address)
                
            except Exception as e:
                print('Exception on socket send %s' % (str(e)))
    
    #----------------------------------------------
    # Entry point            
    def run(self):
        """ Listen for requests """
        
        while not self.__terminate:
            try:
                data, self.__address = self.__sock.recvfrom(100)
                self.__callback(data)
            except socket.timeout:
                continue
            