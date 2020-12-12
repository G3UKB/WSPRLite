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

# All imports
from imports import *

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
    def __init__(self, q, callback):
        """
        Constructor
        
        Arguments:
            q           --  queue on which requests are posted
            callback    --  callback here when data arrives
            
        """

        super(NetIFClient, self).__init__()
        self.__callback = callback
        self.__q = q
        
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.__sock.settimeout(3)
        
        self.__address = (SERVER_IP, SERVER_PORT)
        self.__terminate = False
        
        self.__dispatch = {
            GET_CALLSIGN : self.__get_callsign,
            GET_LOCATOR : self.__get_locator,
            GET_FREQ : self.__get_freq,
            SET_FREQ : self.__set_freq,
            SET_BAND : self.__set_band,
            SET_TX : self.__set_tx,
            SET_IDLE : self.__set_idle
            GET_STATUS : self.__get_status
        }
    
    #----------------------------------------------
    # Terminate
    def terminate(self):
        """ Terminate thread """
        
        self.__terminate = True
    
    #-------------------------------------------------
    # Thread entry point    
    def run(self):
        """ Listen for events """

        # Processing loop
        while not self.__terminate:
            while len(self.__q) > 0:
                cmd, args = self.__q.popleft()
                self.__dispatch[cmd](args)
            sleep(0.1)
            
        print ("WSPRLite Automation - Net thread exiting...")
        
    #=========================================================================
    # Command Execution
    #=========================================================================
    
    #----------------------------------------------
    # Get callsign
    def __get_callsign(self, p):
        """ Return the configured callsign """
        r, data = self.__data_exchange((GET_CALLSIGN,), self.__address)
        if r:
            self.__callback((GET_CALLSIGN, pickle.loads(data)))
        else:
            self.__callback((GET_CALLSIGN, (False, data)))
    
    #----------------------------------------------
    # Get locator
    def __get_locator(self, p):
        """ Return the configured locator """
        r, data = self.__data_exchange((GET_LOCATOR,), self.__address)
        if r:
            self.__callback((GET_LOCATOR, pickle.loads(data)))
        else:
            self.__callback((GET_LOCATOR, (False, data)))
            
    #----------------------------------------------
    # Get actual TX frequency
    def __get_freq(self, p):
        """ Return the actual TX frequency in the selected band """
        r, data = self.__data_exchange((GET_FREQ,), self.__address)
        if r:
            self.__callback((GET_FREQ, pickle.loads(data)))
        else:
            self.__callback((GET_FREQ, (False, data)))
            
    #----------------------------------------------
    # Set TX frequency
    def __set_freq(self, freq):
        """ Sets the TX frequency """
        r, data = self.__data_exchange((SET_FREQ, freq), self.__address)
        if r:
            self.__callback((SET_FREQ, pickle.loads(data)))
        else:
            self.__callback((SET_FREQ, (False, data)))
            
    #----------------------------------------------
    # Set band
    def __set_band(self, band):
        """ Select the band for transmission """
        r, data = self.__data_exchange((SET_BAND, band), self.__address)
        if r:
            self.__callback((SET_BAND, pickle.loads(data)))
        else:
            self.__callback((SET_BAND, (False, data)))

    #----------------------------------------------
    # These are async messages in that the server will wait for the appropriate time
    # to start/stop the cycle. Updates are sent on another UDP channel.
    #----------------------------------------------
    
    #----------------------------------------------
    # Set TX mode
    def __set_tx(self, p):
        """ Set device to tx mode """
        r, data = self.__data_exchange((SET_TX,), self.__address)
        if r:
            self.__callback((SET_TX, pickle.loads(data)))
        else:
            self.__callback((SET_TX, (False, data)))
        
    #----------------------------------------------
    # Set idle
    def __set_idle(self, p):
        """ Effectively turn TX off after the next TX cycle """
        r, data = self.__data_exchange((SET_IDLE,), self.__address)
        if r:
            self.__callback((SET_IDLE, pickle.loads(data)))
        else:
            self.__callback((SET_IDLE, (False, data)))
    
    #----------------------------------------------
    # Get status
    def __get_status
        r, data = self.__data_exchange((GET_STATUS,), self.__address)
        if r:
            self.__callback((GET_STATUS, pickle.loads(data)))
        else:
            self.__callback((GET_STATUS, (False, data)))
            
    #----------------------------------------------
    # Send to device
    def __data_exchange(self, msg, address):
        """ Send the given message over UDP """
        pickledData = pickle.dumps(msg)
        try:
            self.__sock.sendto(pickledData, address)
            data, addr = self.__sock.recvfrom(100)
            return (True, data)
        except socket.timeout:
            return False, "Timeout on read!"
        
'''        
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
'''
