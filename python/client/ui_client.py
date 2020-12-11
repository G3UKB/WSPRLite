#!/usr/bin/env python3
#
# ui_client.py
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

# Application imports
sys.path.append('..')
from common.defs import *
from common.freq_table import *
import netif_client as netif
import webrelay

"""
UI for the WSPRLite client application.
"""
class UIClient(QMainWindow):
    
    def __init__(self, qt_app):
        """
        Constructor
        
        Arguments:
            qt_app  --  the Qt appplication object
            
        """
        
        super(UIClient, self).__init__()
        
        self.__qt_app = qt_app
        
        # Class vars
        self.__liteCallsign = ''
        self.__liteLocator = ''
        self.__liteFreq = ''
        
        # Set the back colour
        palette = QPalette()
        palette.setColor(QPalette.Background,QColor(195,195,195,255))
        self.setPalette(palette)
        
        # Create the net interface and a q to dispatch to
        self.__netq = deque()
        self.__net = netif.NetIFClient(self.__netq, self.__netCallback)
        self.__net.start()
        
        # Initialise the GUI
        self.initUI()
        
        # Init fields
        self.__netq.append((GET_CALLSIGN, None))
        self.__netq.append((GET_LOCATOR, None))
        self.__netq.append((GET_FREQ, None))
        
        # Show the GUI
        self.show()
        self.repaint()
        
        # Set a timer
        QTimer.singleShot(IDLE_TICKER, self.__idleProcessing)
    
    # =====================================================================
    # UI initialisation and window event handlers
    def initUI(self):
        """ Configure the GUI interface """
        
        self.setToolTip('Antenna Switch Controller')
        
        # Arrange window
        self.move(100, 100)
        self.setWindowTitle('WSPRLite Automation')
        
        # Set layout
        w = QWidget()
        self.setCentralWidget(w)
        self.__grid = QGridLayout()
        w.setLayout(self.__grid)
        
        # Create widgets
        lcallsign = QLabel("Callsign")
        self.__grid.addWidget(lcallsign, 0, 0)
        self.wcallsign = QLabel("")
        self.__grid.addWidget(self.wcallsign, 0, 1)
        
        llocator = QLabel("Locator")
        self.__grid.addWidget(llocator, 1, 0)
        self.wlocator = QLabel("")
        self.__grid.addWidget(self.wlocator, 1, 1)
        
        lfreqget = QLabel("Current Freq")
        self.__grid.addWidget(lfreqget, 2, 0)
        self.wfreqget = QLabel("")
        self.__grid.addWidget(self.wfreqget, 2, 1)
        
        lfreqset = QLabel("Set Freq")
        self.__grid.addWidget(lfreqset, 3, 0)
        self.wfreqtoset = QLineEdit('000.000.000')
        self.wfreqtoset.setInputMask('999.999.999')
        self.__grid.addWidget(self.wfreqtoset, 3, 1)
        self.bfreqset = QPushButton('Set')
        self.__grid.addWidget(self.bfreqset, 3, 2)
        self.bfreqset.clicked.connect(self.__freq)
        
        lband = QLabel("Band")
        self.__grid.addWidget(lband, 4, 0)
        self.wband = QComboBox()
        self.wband.addItems(BANDS_AVAILABLE)
        self.__grid.addWidget(self.wband, 4, 1)
        self.bbandset = QPushButton('Set')
        self.__grid.addWidget(self.bbandset, 4, 2)
        self.bbandset.clicked.connect(self.__band)
        
        lcycles = QLabel("Cycles")
        self.__grid.addWidget(lcycles, 5, 0)
        self.wcycles = QSpinBox()
        self.wcycles.setRange(0, 10)
        self.__grid.addWidget(self.wcycles, 5, 1)
        self.wcyclesset = QPushButton('TX')
        self.__grid.addWidget(self.wcyclesset, 5, 2)
    
    # ------------------------------------------------------
    # Run the application
    def run(self, ):
        # Returns when application exists
        print("WSPRLite Automation Client running...")
        return self.__qt_app.exec_()
    
    # ------------------------------------------------------
    # Terminate the application
    def terminate(self, ):
        self.__net.terminate()
        self.__net.join()
        
    # =====================================================================
    # UI Events
    
    # ------------------------------------------------------
    # Freq change
    def __freq(self, ):
        s = self.wfreqtoset.text()
        f = ''
        for i in range(0, len(s)):
            if s[i] != '.':
                f = f + (s[i])
        f = float(f)/1000000.0
        upper, lower, band = find_band(f)
        print(band)
        if band == None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Invalid frequency!")
            msg.setInformativeText("Please select a frequency within the bands you have LPF's available")
            msg.setWindowTitle("Info")
            msg.setDetailedText(get_band_limits())
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
        else:
            if str(band) in BANDS_AVAILABLE:
                # Set lite
                self.__netq.append((SET_FREQ, f))
                # Set the band in drop down but dont send else freq will be reset
                index = self.wband.findText(str(band), Qt.MatchFixedString)
                if index >= 0:
                    self.wband.setCurrentIndex(index)
                    # Set LPF filter
                    webrelay.set_lpf(WEBRELAY_IP, WEBRELAY_PORT, band)
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Invalid band!")
                msg.setInformativeText("Please select a frequency within the bands you have LPF's available")
                msg.setWindowTitle("Info")
                msg.setDetailedText(get_band_limits())
                msg.setStandardButtons(QMessageBox.Ok)
                retval = msg.exec_()
        
    # ------------------------------------------------------
    # Band change
    def __band(self, ):
        band = int(self.wband.currentText())
        self.__netq.append((SET_BAND, band))
        # Set LPF filter
        webrelay.set_lpf(WEBRELAY_IP, WEBRELAY_PORT, band)
    
    #========================================================================================
    # Idle time processing 
    def __idleProcessing(self):
        
        """
        Idle processing.
        Called every 100ms single shot
        
        """
        self.wcallsign.setText(self.__liteCallsign)
        self.wlocator.setText(self.__liteLocator)
        self.wfreqget.setText(self.__liteFreq)
        
        # Set next tick
        QTimer.singleShot(IDLE_TICKER, self.__idleProcessing)
        
    # =====================================================================
    # Callbacks
    
    # ------------------------------------------------------
    # Callback from net interface
    def __netCallback(self, data):
        cmd = data[0]
        flag = data[1][0]
        result = data[1][1]
        
        if flag:
            if cmd == GET_CALLSIGN:
                self.__liteCallsign = result
            elif cmd == GET_LOCATOR:
                self.__liteLocator = result
            elif cmd == GET_FREQ:
                self.__liteFreq = str(result)
            elif cmd == SET_BAND:
                self.__liteFreq = str(result)
        