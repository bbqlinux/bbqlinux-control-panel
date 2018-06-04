#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
sys.path.append('/usr/lib/bbqlinux-control-panel')
sys.path.append('/usr/share/bbqlinux-control-panel')
import os
import string
import settings
import qt_resources_rc

from PyQt4 import QtGui, QtCore, uic

class ControlPanelWindow(QtGui.QMainWindow):

    PAGE_WELCOME = 0
    PAGE_ENVIRONMENT = 1

    def __init__(self, system_bus):
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('/usr/share/bbqlinux-control-panel/qt_interface.ui')

        # Set window title
        self.ui.setWindowTitle("BBQLinux Control Panel")
        self.ui.setWindowIcon(QtGui.QIcon('/usr/share/bbqlinux/icons/bbqlinux_icon_blue_32x32.png'))

        # Get available java versions from backend service
        self.javaSwitcherProxy = system_bus.get_object(settings.DBUS_BUS_NAME, "/JavaSwitcher")
        self.java_available = self.javaSwitcherProxy.GetAvailableJavaVersions()
        print("Java versions available: %s" % self.java_available)

        # Get available python versions from backend service
        self.pythonSwitcherProxy = system_bus.get_object(settings.DBUS_BUS_NAME, "/PythonSwitcher")
        self.python_available = self.pythonSwitcherProxy.GetAvailablePythonVersions()
        print("Python versions available: %s" % self.python_available)

        # Switch to environment page
        self.showPageEnvironment()

        # Show the window
        self.ui.show()
        
        # Move main window to center
        qr = self.ui.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())

        # Connect the buttons
        self.connect(self.ui.pushButton_quit, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.pushButton_pageSelector_environment, QtCore.SIGNAL("clicked()"), self.pushButton_pageSelector_environment_clicked)

        # Connect java switcher buttons
        self.connect(self.ui.comboBox_java, QtCore.SIGNAL("activated(int)"), self.comboBox_java_activated)

        # Connect python switcher buttons
        self.connect(self.ui.comboBox_python, QtCore.SIGNAL("activated(int)"), self.comboBox_python_activated)

    def getCurrentPageIndex(self):
        ''' Get the current page index '''
        return self.ui.pageStack.currentIndex()
    
    def setCurrentPageIndex(self, index):
        ''' Jump to a page index '''
        if (index < self.PAGE_WELCOME):
            index = self.PAGE_WELCOME
        self.ui.pageStack.setCurrentIndex(index)

    def showPageEnvironment(self):
        ''' Show environment page '''
        self.comboBox_java_refresh(self.java_available)
        self.comboBox_python_refresh(self.python_available)
        self.setCurrentPageIndex(self.PAGE_ENVIRONMENT)

    def pushButton_pageSelector_environment_clicked(self):      
        self.showPageEnvironment()

    # Java switcher
    def comboBox_java_refresh(self, available_versions):
        self.ui.comboBox_java.clear()
        active_version = self.javaSwitcherProxy.GetActiveJavaVersion()
        active_index = 0
        print("Active Java version: %s" % active_version)
        idx = -1
        for v in available_versions:
            idx += 1
            print("Adding Java version %s on index %d (%s)" % (v, idx, active_version))
            self.ui.comboBox_java.addItem(v)
            self.ui.comboBox_java.setItemData(idx, v, 32)
            if v == active_version:
                active_index = idx               
        self.ui.comboBox_java.setCurrentIndex(active_index)

    def comboBox_java_activated(self, idx):
        version = self.ui.comboBox_java.itemData(idx)
        if version in self.java_available:
            print("Setting default Java version: %s" % version)
            self.javaSwitcherProxy.SetJavaVersion(version, dbus_interface=settings.DBUS_INTERFACE_NAME)
            self.comboBox_java_refresh(self.java_available)
        else:
            print("Unsupported Java version: %s" % version)
    
    # Python switcher
    def comboBox_python_refresh(self, available_versions):
        self.ui.comboBox_python.clear()
        active_version = int(self.pythonSwitcherProxy.GetActivePythonVersion())
        active_index = 0
        print("Active Python version: %s" % active_version)
        idx = -1
        for v in available_versions:
            idx += 1
            print("Adding Python version %s on index %d" % (v, idx))
            self.ui.comboBox_python.addItem(str(v))
            self.ui.comboBox_python.setItemData(idx, v, 32)
            if v == active_version:
                active_index = idx               
        self.ui.comboBox_python.setCurrentIndex(active_index)

    def comboBox_python_activated(self, idx):
        version = self.ui.comboBox_python.itemData(idx)
        if version in self.python_available:
            print("Setting default Python version: %s" % version)
            self.pythonSwitcherProxy.SetPythonVersion(version, dbus_interface=settings.DBUS_INTERFACE_NAME)
            self.comboBox_python_refresh(self.python_available)
        else:
            print("Unsupported Python version: %s" % version)
