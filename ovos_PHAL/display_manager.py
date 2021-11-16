# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

""" DisplayManager

This module provides basic "state" for the visual representation associated
with this Mycroft instance.  The current states are:
   ActiveSkill - The skill that last interacted with the display via the
                 Enclosure API.

Currently, a wakeword sets the ActiveSkill to "wakeword", which will auto
clear after 10 seconds.

A skill is set to Active when it matches an intent, outputs audio, or
changes the display via the EnclosureAPI()

A skill is automatically cleared from Active two seconds after audio
output is spoken, or 2 seconds after resetting the display.

So it is common to have '' as the active skill.
"""

import json
import os
from threading import Timer

from ovos_utils.log import LOG
from ovos_utils.messagebus import get_mycroft_bus
from ovos_utils.signal import get_ipc_directory


def _write_data(dictionary):
    """ Writes the dictionary of state data to the IPC directory.

    Args:
        dictionary (dict): information to place in the 'disp_info' file
    """

    managerIPCDir = os.path.join(get_ipc_directory(), "managers")
    # change read/write permissions based on if file exists or not
    path = os.path.join(managerIPCDir, "disp_info")
    permission = "r+" if os.path.isfile(path) else "w+"

    if permission == "w+" and os.path.isdir(managerIPCDir) is False:
        os.makedirs(managerIPCDir)
        os.chmod(managerIPCDir, 0o777)

    try:
        with open(path, permission) as dispFile:

            # check if file is empty
            if os.stat(str(dispFile.name)).st_size != 0:
                data = json.load(dispFile)

            else:
                data = {}
                LOG.info("Display Manager is creating " + dispFile.name)

            for key in dictionary:
                data[key] = dictionary[key]

            dispFile.seek(0)
            dispFile.write(json.dumps(data))
            dispFile.truncate()

        os.chmod(path, 0o777)

    except Exception as e:
        LOG.error(e)
        LOG.error("Error found in display manager file, deleting...")
        os.remove(path)
        _write_data(dictionary)


def _read_data():
    """ Writes the dictionary of state data from the IPC directory.
    Returns:
        dict: loaded state information
    """
    managerIPCDir = os.path.join(get_ipc_directory(), "managers")

    path = os.path.join(managerIPCDir, "disp_info")
    permission = "r" if os.path.isfile(path) else "w+"

    if permission == "w+" and os.path.isdir(managerIPCDir) is False:
        os.makedirs(managerIPCDir)

    data = {}
    try:
        with open(path, permission) as dispFile:

            if os.stat(str(dispFile.name)).st_size != 0:
                data = json.load(dispFile)

    except Exception as e:
        LOG.error(e)
        os.remove(path)
        _read_data()

    return data


class DisplayManager:
    """ The Display manager handles the basic state of the display,
    be it a mark-1 or a mark-2 or even a future Mark-3.
    """

    def __init__(self, skill_id=None, bus=None):
        self.skill_id = skill_id or ""
        self._should_remove = True
        self.bus = None
        if bus:
            self.bind(bus)

    def set_active(self, skill_id=None):
        """ Sets skill_id as active in the display Manager
        Args:
            string: skill_id
        """
        skill_id = skill_id if skill_id is not None else self.skill_id
        _write_data({"active_skill": skill_id})

    def get_active(self):
        """ Get the currenlty active skill from the display manager
        Returns:
            string: The active skill's skill_id
        """
        data = _read_data()
        active_skill = ""

        if "active_skill" in data:
            active_skill = data["active_skill"]

        return active_skill

    def remove_active(self):
        """ Clears the active skill """
        LOG.debug("Removing active skill...")
        _write_data({"active_skill": ""})

    def bind(self, bus=None):
        """ Connects the display manager to the messagebus """
        self.bus = bus or get_mycroft_bus()
        self.bus.on('recognizer_loop:audio_output_end', self._set_delay)
        self.bus.on('recognizer_loop:audio_output_start', self._set_remove_flag)
        self.bus.on('recognizer_loop:record_begin', self._set_wakeword_skill)

    def _check_flag(self):
        if self._should_remove:
            self.remove_active()

    def _set_delay(self, event=None):
        self._should_remove = True
        Timer(2, self._check_flag).start()

    def _set_remove_flag(self, event=None):
        self._should_remove = False

    def _remove_wake_word(self):
        data = _read_data()
        if "active_skill" in data and data["active_skill"] == "wakeword":
            self.remove_active()

    def _set_wakeword_skill(self, event=None):
        self.set_active("wakeword")
        Timer(10, self._remove_wake_word).start()

    def shutdown(self):
        if self.bus:
            self.bus.on('recognizer_loop:audio_output_end', self._set_delay)
            self.bus.on('recognizer_loop:audio_output_start', self._set_remove_flag)
            self.bus.on('recognizer_loop:record_begin', self._set_wakeword_skill)
