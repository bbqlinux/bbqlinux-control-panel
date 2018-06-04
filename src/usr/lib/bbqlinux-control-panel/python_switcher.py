#! /usr/bin/env python3
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
import os
import dbus.service
import settings

class PythonSwitcher(dbus.service.Object):

    def __init__(self, controlPanel, path):
        self.controlPanel = controlPanel
        dbus.service.Object.__init__(self, self.controlPanel.system_bus, path)

        self.python_info = self.create_python_info()        
        self.python_symlink = "%s%s" % (self.python_info['python']['path'], self.python_info['python']['exec'])

    def create_python_info(self):
        d = {}
        
        d['python'] = {}
        d['python']['version'] = 0
        d['python']['path'] = '/usr/bin/'
        d['python']['exec'] = 'python'
        
        d['python2'] = {}
        d['python2']['version'] = 2
        d['python2']['path'] = '/usr/bin/'
        d['python2']['exec'] = 'python2'
        
        d['python3'] = {}
        d['python3']['version'] = 3
        d['python3']['path'] = '/usr/bin/'
        d['python3']['exec'] = 'python3'
        
        return d

    def get_available_python_versions(self):
        l = []
        for k, v in self.python_info.items():
            if 'version' in v:
                if v['version'] > 0:
                    if os.path.isfile(("%s%s" % (v['path'], v['exec']))):
                        l.append(v['version'])
        return l

    @dbus.service.method(dbus_interface=settings.DBUS_INTERFACE_NAME,
        in_signature='',
        out_signature='an',
        sender_keyword='sender',
        connection_keyword='conn')
    def GetAvailablePythonVersions(self, sender=None, conn=None):
        self.controlPanel.check_polkit_privilege(sender, conn, "org.bbqlinux.ControlPanel")
        return self.get_available_python_versions()

    @dbus.service.method(dbus_interface=settings.DBUS_INTERFACE_NAME,
        in_signature='',
        out_signature='u',
        sender_keyword='sender',
        connection_keyword='conn')
    def GetActivePythonVersion(self, sender=None, conn=None):
        self.controlPanel.check_polkit_privilege(sender, conn, "org.bbqlinux.ControlPanel")
        try:
            python_path = os.readlink(self.python_symlink)
            if python_path == ("%s%s" % (self.python_info['python2']['path'],
                    self.python_info['python2']['exec'])) or \
                    python_path == ("%s" % self.python_info['python2']['exec']):
                return self.python_info['python2']['version']
            elif python_path == ("%s%s" % (self.python_info['python3']['path'], 
                    self.python_info['python3']['exec'])) or \
                    python_path == ("%s" % self.python_info['python3']['exec']):
                return self.python_info['python3']['version']
            else:
                print("No Python version active")
                return 0
        except Exception as e:
            print(e) 
            pass

        print("No Python version active")
        return 0

    @dbus.service.method(dbus_interface=settings.DBUS_INTERFACE_NAME,
        in_signature='u',
        out_signature='',
        sender_keyword='sender',
        connection_keyword='conn')
    def SetPythonVersion(self, version, sender=None, conn=None):
        self.controlPanel.check_polkit_privilege(sender, conn, "org.bbqlinux.ControlPanel")
        if (version == self.python_info['python2']['version']):
            os.system("rm %s" % self.python_symlink)
            os.system("ln -s %s%s %s" % (self.python_info['python2']['path'], self.python_info['python2']['exec'], self.python_symlink))
        elif (version == self.python_info['python3']['version']):
            os.system("rm %s" % self.python_symlink)
            os.system("ln -s %s%s %s" % (self.python_info['python3']['path'], self.python_info['python3']['exec'], self.python_symlink))
        else:
            print("Unsupported Python version: %d" % version)
