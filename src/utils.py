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
# win32api a été supprimé.
from time import sleep

from configReader import ConfigReader


class Utils:
    def __init__(self):
        self.config = ConfigReader()
        self.reload_config()

        # Les états sont initialisés à False par défaut.
        self.aim_state = False
        self.recoil_state = False

        # Les key_binds ont été retirés car ils dépendaient de win32api.
        # Vous devrez gérer les changements d'état (toggles) via votre nouvelle méthode d'input.

    def check_for_updates(self):
        """
        TODO: Remplacez cette fonction par la logique de votre nouveau système d'input.
        Cette fonction devrait mettre à jour les états comme self.aim_state, etc.
        et retourner True si le programme doit être rechargé.
        """
        # Exemple de logique à implémenter :
        # if my_input_handler.should_reload_config():
        #     return True
        # self.aim_state = my_input_handler.is_aim_toggled()
        # self.recoil_state = my_input_handler.is_recoil_toggled()

        return False # Par défaut, on ne recharge pas la config.

    def reload_config(self):
        self.config.read_config()

    def get_aim_state(self):
        # TODO: Implémentez la logique pour savoir si l'aim doit être actif.
        # Doit retourner True si la (ou les) touche(s) d'aim sont pressées.
        return self.aim_state

    def get_trigger_state(self):
        # TODO: Implémentez la logique pour savoir si le triggerbot doit être actif.
        return False

    def get_rapid_fire_state(self):
        # TODO: Implémentez la logique pour savoir si le rapid fire doit être actif.
        return False

    def is_shooting(self):
        # TODO: Implémentez la logique pour savoir si l'utilisateur est en train de tirer.
        # Ceci est nécessaire pour le recul.
        return False

    @staticmethod
    def print_attributes(obj):
        attributes = vars(obj)
        for attribute, value in attributes.items():
            print(f'{attribute}: {value}')