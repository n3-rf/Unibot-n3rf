from configparser import ConfigParser
import numpy as np
import os


class ConfigReader:
    def __init__(self):
        self.parser = ConfigParser()

        # Screen
        self.detection_threshold = None
        # self.upper_color et self.lower_color ont été supprimés
        self.fov_x = None
        self.fov_y = None
        self.aim_fov_x = None
        self.aim_fov_y = None
        self.fps = None
        self.auto_detect_resolution = None
        self.resolution_x = None
        self.resolution_y = None

        # Detection (Nouvelle section)
        self.health_bar_lower_color_1 = None
        self.health_bar_upper_color_1 = None
        self.health_bar_lower_color_2 = None
        self.health_bar_upper_color_2 = None
        self.health_bar_aspect_ratio = None
        self.health_bar_min_area = None
        self.health_bar_max_area = None
        self.player_outline_lower_color_1 = None
        self.player_outline_upper_color_1 = None
        self.player_outline_lower_color_2 = None
        self.player_outline_upper_color_2 = None
        self.roi_height_multiplier = None

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

        # Debug
        self.debug = None
        self.debug_always_on = None
        self.display_mode = None

        # Get config path and read it
        self.path = os.path.join(os.path.dirname(__file__), '../config.ini')
        self.parser.read(self.path)

    def read_config(self):
        # --- Helper function pour parser les couleurs ---
        def parse_color(color_str):
            parts = color_str.split(',')
            return np.array([int(p.strip()) for p in parts])

        # --- Get screen settings ---
        values_str = self.parser.get('screen', 'detection_threshold').split(',')
        self.detection_threshold = (int(values_str[0].strip()), int(values_str[1].strip()))

        # Les anciennes lignes pour upper_color et lower_color ont été supprimées

        self.fov_x = self.parser.getint('screen', 'fov_x')
        self.fov_y = self.parser.getint('screen', 'fov_y')
        self.aim_fov_x = self.parser.getint('screen', 'aim_fov_x')
        self.aim_fov_y = self.parser.getint('screen', 'aim_fov_y')
        fps_value = self.parser.getint('screen', 'fps')
        self.fps = int(np.floor(1000 / fps_value + 1))
        self.auto_detect_resolution = self.parser.getboolean('screen', 'auto_detect_resolution')
        self.resolution_x = self.parser.getint('screen', 'resolution_x')
        self.resolution_y = self.parser.getint('screen', 'resolution_y')

        # --- Get detection settings ---
        self.health_bar_lower_color_1 = parse_color(self.parser.get('detection', 'health_bar_lower_color_1'))
        self.health_bar_upper_color_1 = parse_color(self.parser.get('detection', 'health_bar_upper_color_1'))
        self.health_bar_lower_color_2 = parse_color(self.parser.get('detection', 'health_bar_lower_color_2'))
        self.health_bar_upper_color_2 = parse_color(self.parser.get('detection', 'health_bar_upper_color_2'))

        self.health_bar_aspect_ratio = self.parser.getfloat('detection', 'health_bar_aspect_ratio')
        self.health_bar_min_area = self.parser.getint('detection', 'health_bar_min_area')
        self.health_bar_max_area = self.parser.getint('detection', 'health_bar_max_area')

        self.player_outline_lower_color_1 = parse_color(self.parser.get('detection', 'player_outline_lower_color_1'))
        self.player_outline_upper_color_1 = parse_color(self.parser.get('detection', 'player_outline_upper_color_1'))
        self.player_outline_lower_color_2 = parse_color(self.parser.get('detection', 'player_outline_lower_color_2'))
        self.player_outline_upper_color_2 = parse_color(self.parser.get('detection', 'player_outline_upper_color_2'))

        self.roi_height_multiplier = self.parser.getfloat('detection', 'roi_height_multiplier')

        # --- Get aim settings ---
        self.offset = self.parser.getint('aim', 'offset')
        value = self.parser.getfloat('aim', 'smooth')
        if 0 <= value <= 1:
            self.smooth = 1 - value / 1.25
        else:
            print('WARNING: Invalid smooth value')
        self.speed = self.parser.getfloat('aim', 'speed')
        self.y_speed = self.parser.getfloat('aim', 'y_speed')
        value = self.parser.getfloat('aim', 'aim_height')
        if 0 <= value <= 1:
            self.aim_height = value
        else:
            print('WARNING: Invalid aim_height value')

        # --- Get recoil settings ---
        self.recoil_mode = self.parser.get('recoil', 'mode').lower()
        self.recoil_x = self.parser.getfloat('recoil', 'recoil_x')
        self.recoil_y = self.parser.getfloat('recoil', 'recoil_y')
        self.max_offset = self.parser.getint('recoil', 'max_offset')
        self.recoil_recover = self.parser.getfloat('recoil', 'recover')

        # --- Get trigger settings ---
        self.trigger_delay = self.parser.getint('trigger', 'trigger_delay')
        self.trigger_randomization = self.parser.getint('trigger', 'trigger_randomization')
        self.trigger_threshold = self.parser.getint('trigger', 'trigger_threshold')

        # --- Get rapid fire settings ---
        self.target_cps = self.parser.getint('rapid_fire', 'target_cps')

        # --- Get debug settings ---
        self.debug = self.parser.getboolean('debug', 'enabled')
        self.debug_always_on = self.parser.getboolean('debug', 'always_on')
        self.display_mode = self.parser.get('debug', 'display_mode').lower()