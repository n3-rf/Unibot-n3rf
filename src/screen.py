"""
    Unibot, an open-source colorbot.
    Copyright (C) 2025 vike256
    (Licence GPLv3)
"""
import cv2
import numpy as np
import bettercam
from pyautogui import size
import time

class Screen:
    def __init__(self, config):
        self.cam = bettercam.create(output_color="BGR")

        self.offset = config.offset

        if config.auto_detect_resolution:
            screen_size = size()
            self.screen = (screen_size.width, screen_size.height)
        else:
            self.screen = (config.resolution_x, config.resolution_y)

        self.screen_center = (self.screen[0] // 2, self.screen[1] // 2)
        self.screen_region = (0, 0, self.screen[0], self.screen[1])

        self.fov = (config.fov_x, config.fov_y)
        self.fov_center = (self.fov[0] // 2, self.fov[1] // 2)
        self.fov_region = (
            self.screen_center[0] - self.fov[0] // 2,
            self.screen_center[1] - self.fov[1] // 2 - self.offset,
            self.screen_center[0] + self.fov[0] // 2,
            self.screen_center[1] + self.fov[1] // 2 - self.offset
        )

        # --- CHARGEMENT DES PARAMÈTRES DE DÉTECTION ---
        # NOTE: Assurez-vous d'avoir mis à jour votre fichier configReader.py
        # pour qu'il lise toutes les valeurs de la section [detection] !
        self.health_bar_lower_1 = config.health_bar_lower_color_1
        self.health_bar_upper_1 = config.health_bar_upper_color_1
        self.health_bar_lower_2 = config.health_bar_lower_color_2
        self.health_bar_upper_2 = config.health_bar_upper_color_2
        self.health_bar_aspect_ratio = config.health_bar_aspect_ratio
        self.health_bar_min_area = config.health_bar_min_area
        self.health_bar_max_area = config.health_bar_max_area

        self.player_outline_lower_1 = config.player_outline_lower_color_1
        self.player_outline_upper_1 = config.player_outline_upper_color_1
        self.player_outline_lower_2 = config.player_outline_lower_color_2
        self.player_outline_upper_2 = config.player_outline_upper_color_2

        self.roi_height_multiplier = config.roi_height_multiplier
        # --- FIN DU CHARGEMENT ---

        self.fps = config.fps
        self.debug = config.debug
        self.target = None
        self.img = None
        self.trigger_threshold = config.trigger_threshold
        self.aim_fov = (config.aim_fov_x, config.aim_fov_y)
        self.prev_frame_time = 0

        # Pour le debug
        self.closest_contour_for_debug = None
        self.roi_rect_for_debug = None

        if self.debug:
            self.display_mode = config.display_mode
            self.window_name = 'Unibot Debug'
            self.window_resolution = (self.screen[0] // 2, self.screen[1] // 2)
            cv2.namedWindow(self.window_name)

    def __del__(self):
        if self.debug:
            cv2.destroyAllWindows()
        del self.cam

    def screenshot(self, region):
        image = self.cam.grab(region)
        if image is None:
            return None # Retourne None si la capture échoue
        return np.array(image)

    def get_target(self, recoil_offset):
        recoil_offset = int(recoil_offset)
        self.target = None
        self.roi_rect_for_debug = None
        best_health_bar = None

        self.img = self.screenshot(self.get_region(self.fov_region, recoil_offset))
        if self.img is None:
            return None, False

        hsv = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        # --- ÉTAPE 1: DÉTECTER LES BARRES DE VIE ---
        health_mask_1 = cv2.inRange(hsv, self.health_bar_lower_1, self.health_bar_upper_1)
        health_mask_2 = cv2.inRange(hsv, self.health_bar_lower_2, self.health_bar_upper_2)
        health_mask = cv2.bitwise_or(health_mask_1, health_mask_2)
        health_contours, _ = cv2.findContours(health_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detected_health_bars = []
        for contour in health_contours:
            x, y, w, h = cv2.boundingRect(contour)
            if h > 0:
                area = w * h
                aspect_ratio = w / h
                if self.health_bar_aspect_ratio < aspect_ratio and self.health_bar_min_area < area < self.health_bar_max_area:
                    detected_health_bars.append(contour)

        # --- ÉTAPE 2: SÉLECTIONNER LA MEILLEURE BARRE DE VIE (la plus proche du centre) ---
        if detected_health_bars:
            min_distance = float('inf')
            for bar_contour in detected_health_bars:
                x, y, w, h = cv2.boundingRect(bar_contour)
                center_x, center_y = x + w / 2, y + h / 2
                distance = np.sqrt((center_x - self.fov_center[0])**2 + (center_y - self.fov_center[1])**2)

                if distance < min_distance:
                    min_distance = distance
                    best_health_bar = bar_contour

        # --- ÉTAPE 3: DÉFINIR LA ROI ET TROUVER LE JOUEUR DEDANS ---
        if best_health_bar is not None:
            self.closest_contour_for_debug = best_health_bar
            x_bar, y_bar, w_bar, h_bar = cv2.boundingRect(best_health_bar)

            roi_x = max(0, x_bar - w_bar // 2)
            roi_y = y_bar + h_bar
            roi_w = w_bar * 2
            roi_h = int(h_bar * self.roi_height_multiplier)
            self.roi_rect_for_debug = (roi_x, roi_y, roi_w, roi_h)

            player_mask_1 = cv2.inRange(hsv, self.player_outline_lower_1, self.player_outline_upper_1)
            player_mask_2 = cv2.inRange(hsv, self.player_outline_lower_2, self.player_outline_upper_2)
            player_mask = cv2.bitwise_or(player_mask_1, player_mask_2)

            roi_mask_image = np.zeros(self.img.shape[:2], dtype=np.uint8)
            cv2.rectangle(roi_mask_image, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), 255, -1)
            player_mask_in_roi = cv2.bitwise_and(player_mask, player_mask, mask=roi_mask_image)
            player_contours, _ = cv2.findContours(player_mask_in_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if player_contours:
                best_player_contour = max(player_contours, key=cv2.contourArea)

                # --- ÉTAPE 4: CALCULER LA CIBLE FINALE ---
                topmost_point = min(best_player_contour, key=lambda p: p[0][1])[0]
                final_x = topmost_point[0] - self.fov_center[0]
                final_y = topmost_point[1] - self.fov_center[1]

                if -self.aim_fov[0] <= final_x <= self.aim_fov[0] and -self.aim_fov[1] <= final_y <= self.aim_fov[1]:
                    self.target = (final_x, final_y)

        if self.debug:
            self.debug_display()

        # La logique de 'trigger' a été simplifiée
        return self.target, False

    @staticmethod
    def get_region(region, recoil_offset):
        return (region[0], region[1] - recoil_offset, region[2], region[3] - recoil_offset)

    def debug_display(self):
        debug_img = self.img.copy()

        # Dessiner la barre de vie détectée en bleu
        if self.closest_contour_for_debug is not None:
            x, y, w, h = cv2.boundingRect(self.closest_contour_for_debug)
            cv2.rectangle(debug_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Dessiner la zone de recherche (ROI) en jaune
        if self.roi_rect_for_debug is not None:
            rx, ry, rw, rh = self.roi_rect_for_debug
            cv2.rectangle(debug_img, (rx, ry), (rx + rw, ry + rh), (0, 255, 255), 1)

        # Dessiner la cible finale en vert
        if self.target is not None:
            target_abs_x = self.target[0] + self.fov_center[0]
            target_abs_y = self.target[1] + self.fov_center[1]
            cv2.circle(debug_img, (target_abs_x, target_abs_y), 5, (0, 255, 0), -1)
            cv2.line(debug_img, self.fov_center, (target_abs_x, target_abs_y), (0, 255, 0), 2)

        cv2.imshow(self.window_name, debug_img)
        cv2.waitKey(1)