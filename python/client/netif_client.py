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

# Client net interface to the WSPRLite server

# Python imports
import os, sys
import threading
import socket
import pickle
from time import sleep

# Application imports
sys.path.append('..')
from common.defs import *

"""
Client Interface to the WSPRLite server application:

Commands are UDP:
    
"""

#========================================================================
# Net interface
class NetIFClient(threading.Thread):
    
    #----------------------------------------------
    # Constructor
    def __init__(self, callback):
        """
        Constructor
        
        Arguments:
            callback    --  callback here when data arrives
            
        """

        super(NetIFClient, self).__init__()
        self.__callback = callback
        
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(3)
        
        self.__address = None
        self.__terminate = False
    
    #----------------------------------------------
    # Terminate
    def terminate(self):
        """ Terminate thread """
        
        self.__terminate = True
    
    #=========================================================================
    # EXTERNAL INTERFACE
    ##=========================================================================
    
    #----------------------------------------------
    # Get callsign
    def get_callsign(self):
        """ Return the configured callsign """
        data, sender = self.__data_exchange((GET_CALLSIGN,), (SERVER_IP, SERVER_PORT))
        print(pickle.loads(data))
    
    #----------------------------------------------
    # Get locator
    def get_locator(self):
        """ Return the configured locator """
        data, sender = self.__data_exchange((GET_LOCATOR,), (SERVER_IP, SERVER_PORT))
        print(pickle.loads(data))
    
    #----------------------------------------------
    # Get actual TX frequency
    def get_freq(self):
        """ Return the actual TX frequency in the selected band """
        data, sender = self.__data_exchange((GET_FREQ,), (SERVER_IP, SERVER_PORT))
        print(pickle.loads(data))
    
    #----------------------------------------------
    # Set band
    def set_band(self):
        """ Select the band for transmission """
        data, sender = self.__data_exchange((SET_BAND,), (SERVER_IP, SERVER_PORT))
        print(pickle.loads(data))

    #----------------------------------------------
    # These are async messages in that the server will wait for the appropriate time
    # to start/stop cycle. Updates are send on another |UDP channel.
    #----------------------------------------------
    
    #----------------------------------------------
    # Set TX mode
    def set_tx(self):
        """ Set device to tx mode """
        data, sender = self.__data_exchange((SET_TX,), (SERVER_IP, SERVER_PORT))
        print(pickle.loads(data))
        
    #----------------------------------------------
    # Set idle
    def set_idle(self):
        """ Effectively turn TX off after the next TX cycle """
        data, sender = self.__data_exchange((SET_IDLE,), (SERVER_IP, SERVER_PORT))
        print(pickle.loads(data))
    
    #=========================================================================
    # PRIVATE
    #=========================================================================
    
    #----------------------------------------------
    # Send to device
    def __data_exchange(self, msg, address):
        """ Send the given message over UDP """
        pickledData = pickle.dumps(msg)
        sock.sendto(pickledData, address)
        return sock.recvfrom(100)
        
        
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = (SERVER_IP, SERVER_PORT)

pickledData = pickle.dumps((GET_LOCATOR,))
sock.sendto(pickledData, address)
data, sender = sock.recvfrom(100)
print(pickle.loads(data))

pickledData = pickle.dumps((GET_FREQ,))
sock.sendto(pickledData, address)
data, sender = sock.recvfrom(100)
print(pickle.loads(data))

pickledData = pickle.dumps((SET_BAND, 160))
sock.sendto(pickledData, address)
data, sender = sock.recvfrom(100)
print(pickle.loads(data))

pickledData = pickle.dumps((GET_FREQ,))
sock.sendto(pickledData, address)
data, sender = sock.recvfrom(100)
print(pickle.loads(data))

pickledData = pickle.dumps((SET_TX,))
sock.sendto(pickledData, address)
resp = sock.recvfrom(100)
print(resp)
if resp == None:
    while True:
        resp = sock.recvfrom(100)
        if resp != None:
            break
        else:
            print("Waiting response to SET_TX...")
            sleep(10)    
print(pickle.loads(resp[0]))

sleep(3)

pickledData = pickle.dumps((SET_IDLE,))
sock.sendto(pickledData, address)
resp = sock.recvfrom(100)
if resp == None:
    while True:
        resp = sock.recvfrom(100)
        if resp != None:
            break
        else:
            print("Waiting response to SET_IDLE...")
            sleep(10)    
print(pickle.loads(resp[0]))

