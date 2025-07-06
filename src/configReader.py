"""
    Unibot, an open-source colorbot.
    Copyright (C) 2025 vike256

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from configparser import ConfigParser
import numpy as np
import os


class ConfigReader:
    def __init__(self):
        self.parser = ConfigParser()

        # La section Communication a été supprimée
        # Screen
        self.detection_threshold = None
        self.upper_color = None
        self.lower_color = None
        self.fov_x = None
        self.fov_y = None
        self.aim_fov_x = None
        self.aim_fov_y = None
        self.fps = None
        self.auto_detect_resolution = None
        self.resolution_x = None
        self.resolution_y = None

        # Aim
        self.offset = None
        self.smooth = None
        self.speed = None
        self.y_speed = None
        self.aim_height = None

        # Recoil
        self.recoil_mode = None
        self.recoil_x = None
        self.recoil_y = None
        self.max_offset = None
        self.recoil_recover = None

        # Trigger
        self.trigger_delay = None
        self.trigger_randomization = None
        self.trigger_threshold = None

        # Rapid fire
        self.target_cps = None

        # La section Key binds a été supprimée

        # Debug
        self.debug = None
        self.debug_always_on = None
        self.display_mode = None

        # Get config path and read it
        self.path = os.path.join(os.path.dirname(__file__), '../config.ini')
        self.parser.read(self.path)

    def read_config(self):
        # La lecture des paramètres de communication a été supprimée.

        # Get screen settings
        values_str = self.parser.get('screen', 'detection_threshold').split(',')
        self.detection_threshold = (int(values_str[0].strip()), int(values_str[1].strip()))

        upper_color = self.parser.get('screen', 'upper_color').split(',')
        lower_color = self.parser.get('screen', 'lower_color').split(',')
        for i in range(0, 3):
            upper_color[i] = int(upper_color[i].strip())
        for i in range(0, 3):
            lower_color[i] = int(lower_color[i].strip())
        self.upper_color = np.array(upper_color)
        self.lower_color = np.array(lower_color)

        self.fov_x = int(self.parser.get('screen', 'fov_x'))
        self.fov_y = int(self.parser.get('screen', 'fov_y'))
        self.aim_fov_x = int(self.parser.get('screen', 'aim_fov_x'))
        self.aim_fov_y = int(self.parser.get('screen', 'aim_fov_y'))
        fps_value = int(self.parser.get('screen', 'fps'))
        self.fps = int(np.floor(1000 / fps_value + 1))

        value = self.parser.get('screen', 'auto_detect_resolution').lower()
        if value == 'true':
            self.auto_detect_resolution = True
        else:
            self.auto_detect_resolution = False

        self.resolution_x = int(self.parser.get('screen', 'resolution_x'))
        self.resolution_y = int(self.parser.get('screen', 'resolution_y'))

        # Get aim settings
        self.offset = int(self.parser.get('aim', 'offset'))

        value = float(self.parser.get('aim', 'smooth'))
        if 0 <= value <= 1:
            self.smooth = 1 - value / 1.25
        else:
            print('WARNING: Invalid smooth value')

        self.speed = float(self.parser.get('aim', 'speed'))
        self.y_speed = float(self.parser.get('aim', 'y_speed'))

        value = float(self.parser.get('aim', 'aim_height'))
        if 0 <= value <= 1:
            self.aim_height = value
        else:
            print('WARNING: Invalid aim_height value')

        # Get recoil settings
        value = self.parser.get('recoil', 'mode').lower()
        recoil_mode_list = ['move', 'offset']
        if value in recoil_mode_list:
            self.recoil_mode = value
        else:
            print('WARNING: Invalid recoil_mode value')

        self.recoil_x = float(self.parser.get('recoil', 'recoil_x'))
        self.recoil_y = float(self.parser.get('recoil', 'recoil_y'))
        self.max_offset = int(self.parser.get('recoil', 'max_offset'))
        self.recoil_recover = float(self.parser.get('recoil', 'recover'))

        # Get trigger settings
        self.trigger_delay = int(self.parser.get('trigger', 'trigger_delay'))
        self.trigger_randomization = int(self.parser.get('trigger', 'trigger_randomization'))
        self.trigger_threshold = int(self.parser.get('trigger', 'trigger_threshold'))

        # Get rapid fire settings
        self.target_cps = int(self.parser.get('rapid_fire', 'target_cps'))

        # La lecture des keybinds a été supprimée.

        # Get debug settings
        value = self.parser.get('debug', 'enabled').lower()
        if value == 'true':
            self.debug = True
        else:
            self.debug = False

        value = self.parser.get('debug', 'always_on').lower()
        if value == 'true':
            self.debug_always_on = True
        else:
            self.debug_always_on = False

        value = self.parser.get('debug', 'display_mode').lower()
        display_mode_list = ['game', 'mask']
        if value in display_mode_list:
            self.display_mode = value
        else:
            print('WARNING: Invalid display_mode value')

# La fonction read_hex n'est plus utilisée et a été supprimée.