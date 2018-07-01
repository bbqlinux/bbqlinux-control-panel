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
import os
import dbus.service
import settings
import subprocess
import re

class JavaSwitcher(dbus.service.Object):

    def __init__(self, controlPanel, path):
        self.controlPanel = controlPanel
        dbus.service.Object.__init__(self, self.controlPanel.system_bus, path)
        self.available_versions = []

    # Get available java versions
    def get_available_java_versions(self):
        self.available_versions.clear()
        try:
            command_stdout = subprocess.Popen(['archlinux-java', 'status'], stdout=subprocess.PIPE).communicate()[0]
            command_text = command_stdout.decode(encoding='utf-8')

            versions = [x for x in re.split('\n| ', command_text) if x!='']

            for v in versions:
                if (v.startswith('java')):
                    self.available_versions.append(v)

            print("Supported Java versions: %s" % self.available_versions)
        except:
            print("Unexpected error: %s" % sys.exc_info()[1])
            pass

        return self.available_versions

    @dbus.service.method(dbus_interface=settings.DBUS_INTERFACE_NAME,
        in_signature='',
        out_signature='as',
        sender_keyword='sender',
        connection_keyword='conn')
    def GetAvailableJavaVersions(self, sender=None, conn=None):
        self.controlPanel.check_polkit_privilege(sender, conn, "org.bbqlinux.ControlPanel")
        return self.get_available_java_versions()

    # Get active java version
    def get_active_java_version(self):
        active_version = None
        try:
            command_stdout = subprocess.Popen(['archlinux-java', 'get'], stdout=subprocess.PIPE).communicate()[0]
            command_text = command_stdout.decode(encoding='utf-8')
            versions = [x for x in re.split('\n| ', command_text) if x!='']
            for v in versions:
                if (v.startswith('java')):
                    active_version = v
            print("Active Java version: %s" % active_version)
        except:
            print("Unexpected error: %s" % sys.exc_info()[1])
            pass
        return active_version

    @dbus.service.method(dbus_interface=settings.DBUS_INTERFACE_NAME,
        in_signature='',
        out_signature='s',
        sender_keyword='sender',
        connection_keyword='conn')
    def GetActiveJavaVersion(self, sender=None, conn=None):
        self.controlPanel.check_polkit_privilege(sender, conn, "org.bbqlinux.ControlPanel")
        return self.get_active_java_version()

    @dbus.service.method(dbus_interface=settings.DBUS_INTERFACE_NAME,
        in_signature='s',
        out_signature='b',
        sender_keyword='sender',
        connection_keyword='conn')
    def SetJavaVersion(self, version, sender=None, conn=None):
        self.controlPanel.check_polkit_privilege(sender, conn, "org.bbqlinux.ControlPanel")
        if version in self.available_versions:
            os.system("archlinux-java set %s" % version)
        else:
            print("Unsupported Java version: %s" % version)
            return False
        
        new_version = self.get_active_java_version()
        if new_version == version:
            print("Successfully set new Java version: %s" % new_version)
            return True
        else:
            print("Failed setting new Java version")
            return False
