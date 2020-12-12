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
        self.__liteFreq = 0
        self.__connected = False
        self.__lastState = False
        self.__txstatus = IDLE
        
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
        
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        #self.statusBar.showMessage("Not connected")
        self.bmessage = QLabel("Not connected")
        self.bmessage.setStyleSheet("color: red; font: 14px")
        self.btime = QLabel("")
        self.btime.setStyleSheet("color: blue; font: 14px")
        self.statusBar.addWidget(self.bmessage)
        self.statusBar.addPermanentWidget(self.btime)
        
        # Set layout
        w = QWidget()
        self.setCentralWidget(w)
        self.__grid = QGridLayout()
        w.setLayout(self.__grid)
        
        # Create widgets
        lcallsign = QLabel("Callsign")
        self.__grid.addWidget(lcallsign, 0, 0)
        self.wcallsign = QLabel("")
        self.wcallsign.setStyleSheet("color: green; font: 16px")
        self.__grid.addWidget(self.wcallsign, 0, 1)
        
        llocator = QLabel("Locator")
        self.__grid.addWidget(llocator, 1, 0)
        self.wlocator = QLabel("")
        self.wlocator.setStyleSheet("color: green; font: 16px")
        self.__grid.addWidget(self.wlocator, 1, 1)
        
        lfreqget = QLabel("Current Freq")
        self.__grid.addWidget(lfreqget, 2, 0)
        self.wfreqget = QLabel("")
        self.wfreqget.setStyleSheet("color: red; font: 16px")
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
        
        ltx = QLabel("TX")
        self.__grid.addWidget(ltx, 5, 0)
        self.btx = QPushButton('Start')
        self.btx.setCheckable(True)
        self.btx.setStyleSheet("color: green; font: 14px")
        self.__grid.addWidget(self.btx, 5, 1)
        self.btx.clicked.connect(self.__run)
        self.ltxstate = QLabel(self.__txstatus)
        self.ltxstate.setStyleSheet("color: green; font: 14px")
        self.__grid.addWidget(self.ltxstate, 5, 2)
    
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
                    r = webrelay.set_lpf(WEBRELAY_IP, WEBRELAY_PORT, band)
                    if not r[0]:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Information)
                        msg.setText("LPF Failure!")
                        msg.setInformativeText("Failed to select LPF filter.")
                        msg.setWindowTitle("Info")
                        msg.setDetailedText(r[1])
                        msg.setStandardButtons(QMessageBox.Ok)
                        retval = msg.exec_()
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
        r = webrelay.set_lpf(WEBRELAY_IP, WEBRELAY_PORT, band)
        if not r[0]:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("LPF Failure!")
            msg.setInformativeText("Failed to select LPF filter.")
            msg.setWindowTitle("Info")
            msg.setDetailedText(r[1])
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()
    
    # ------------------------------------------------------
    # TX Control
    def __run(self, ):
        if self.btx.isChecked():
            self.__netq.append((SET_TX, None))
            self.btx.setText("Stop")
            self.btx.setStyleSheet("color: red; font: 14px")
        else:
            self.__netq.append((SET_IDLE, None))
            self.btx.setText("Start")
            self.btx.setStyleSheet("color: green; font: 14px")
        
    #========================================================================================
    # Idle time processing 
    def __idleProcessing(self):
        
        """
        Idle processing.
        Called every 100ms single shot
        
        """
    
        # Manage status
        if self.__lastState != self.__connected:
            if self.__connected:
                # Set info
                self.wcallsign.setText(self.__liteCallsign)
                self.wlocator.setText(self.__liteLocator)
                f = float(self.__liteFreq)/1000000.0
                self.wfreqget.setText(str(f))
                # Set band according to frequency device is set to
                upper, lower, band = find_band(f)
                if str(band) in BANDS_AVAILABLE:
                    # Set the band in drop down but dont send else freq will be reset
                    index = self.wband.findText(str(band), Qt.MatchFixedString)
                    if index >= 0:
                        self.wband.setCurrentIndex(index)
                        # Set LPF filter
                        r = webrelay.set_lpf(WEBRELAY_IP, WEBRELAY_PORT, band)
                        if not r[0]:
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Information)
                            msg.setText("LPF Failure!")
                            msg.setInformativeText("Failed to select LPF filter.")
                            msg.setWindowTitle("Info")
                            msg.setDetailedText(r[1])
                            msg.setStandardButtons(QMessageBox.Ok)
                            retval = msg.exec_()
                # Enable buttons
                self.bfreqset.setEnabled(True)
                self.bbandset.setEnabled(True)
                self.btx.setEnabled(True)
                # Tell user
                self.bmessage.setText("Connected")
                self.bmessage.setStyleSheet("color: green; font: 14px")
            else:
                # Try again
                self.__netq.append((GET_CALLSIGN, None))
                self.__netq.append((GET_LOCATOR, None))
                self.__netq.append((GET_FREQ, None))
                # Disable buttons
                self.bfreqset.setEnabled(False)
                self.bbandset.setEnabled(False)
                self.btx.setEnabled(False)
                # Tell user
                self.bmessage.setText("Not Connected!")
                self.bmessage.setStyleSheet("color: red; font: 14px")
            # Update state
            self.__lastState = self.__connected
            
        # Update time
        self.btime.setText(time.strftime("%H"+":"+"%M"+":"+"%S"))
        
        # Update TX status
        self.__netq.append((GET_STATUS, None))
        self.ltxstate.setText(self.__txstatus)
        if self.__txstatus == IDLE:
            self.ltxstate.setStyleSheet("color: green; font: 14px")
        elif self.__txstatus == WAIT_START or self.__txstatus == WAIT_STOP:
            self.ltxstate.setStyleSheet("color: amber; font: 14px")
        elif self.__txstatus == TX_CYCLING:
            self.ltxstate.setStyleSheet("color: red; font: 14px")
        
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
        print(cmd, flag, result)
        if flag:
            self.__connected = True
            if cmd == GET_CALLSIGN:
                self.__liteCallsign = result
            elif cmd == GET_LOCATOR:
                self.__liteLocator = result
            elif cmd == GET_FREQ:
                self.__liteFreq = str(result)
            elif cmd == SET_BAND:
                self.__liteFreq = str(result)
            elif cmd == GET_STATUS:
                self.__txstatus = result
        else:
            self.__connected = False
        