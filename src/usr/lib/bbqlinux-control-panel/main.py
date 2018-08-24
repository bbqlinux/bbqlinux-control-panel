#!/usr/bin/env python3
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
import dbus
import settings

from PyQt5 import QtCore, QtWidgets
from ui.qt_interface import ControlPanelWindow

# main entry
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = ControlPanelWindow(sys.argv[1:], dbus.SystemBus())
    sys.exit(app.exec_())
