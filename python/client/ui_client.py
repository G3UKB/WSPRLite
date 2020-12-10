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
        
        # Set the back colour
        palette = QPalette()
        palette.setColor(QPalette.Background,QColor(195,195,195,255))
        self.setPalette(palette)
        
        # Initialise the GUI
        self.initUI()
        
        # Show the GUI
        self.show()
        self.repaint()
    
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
        
        lfreq = QLabel("Freq")
        self.__grid.addWidget(lfreq, 2, 0)
        self.wfreq = QLineEdit('000.000.000')
        self.wfreq.setInputMask('999.999.999')
        self.__grid.addWidget(self.wfreq, 2, 1)
        self.wfreqset = QPushButton('Set')
        self.__grid.addWidget(self.wfreqset, 2, 2)
        
        lband = QLabel("Band")
        self.__grid.addWidget(lband, 3, 0)
        self.wband = QComboBox()
        self.wband.addItems(['160','80','40','20','15', '10'])
        self.__grid.addWidget(self.wband, 3, 1)
        self.wbandset = QPushButton('Set')
        self.__grid.addWidget(self.wbandset, 3, 2)
        
        lcycles = QLabel("Cycles")
        self.__grid.addWidget(lcycles, 4, 0)
        self.wcycles = QSpinBox()
        self.wcycles.setRange(0, 10)
        self.__grid.addWidget(self.wcycles, 4, 1)
        self.wcyclesset = QPushButton('TX')
        self.__grid.addWidget(self.wcyclesset, 4, 2)
    
    def run(self, ):
        """ Run the application """
        
        # Returns when application exists
        print("WSPRLite Automation Client running...")
        return self.__qt_app.exec_()    