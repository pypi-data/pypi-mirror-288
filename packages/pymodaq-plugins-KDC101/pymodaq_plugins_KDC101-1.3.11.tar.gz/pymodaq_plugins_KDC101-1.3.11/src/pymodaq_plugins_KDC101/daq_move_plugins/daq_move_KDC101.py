from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun, main,
                                                          DataActuatorType, DataActuator)
import clr
import os
import sys
import time
from System import Decimal, Int32

# Importer les bibliothèques Kinesis
dll_path = r'C:\Program Files\Thorlabs\Kinesis'
if dll_path not in sys.path:
    sys.path.append(dll_path)

clr.AddReference('Thorlabs.MotionControl.DeviceManagerCLI')
clr.AddReference('Thorlabs.MotionControl.KCube.DCServoCLI')
clr.AddReference('Thorlabs.MotionControl.GenericMotorCLI')

from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.DCServoCLI import KCubeDCServo
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import VelocityParameters

class KCubeDCServoController:
    def __init__(self):
        # Initialiser le gestionnaire de périphériques
        DeviceManagerCLI.BuildDeviceList()

        # Obtenir la liste des périphériques
        self.device_list = DeviceManagerCLI.GetDeviceList()

        # Convertir la liste en liste Python pour un affichage correct
        self.device_list_python = [str(device) for device in self.device_list]

        # Initialiser l'ID du périphérique à None
        self.device_id = None
        self.motor = None
        self.distance_total = 2
        self.temps_total_s = 0.0
        self.temps_total_s_d = None
        self.vitesse = 2
        self.distance_precedente = None  # Distance précédente initialisée à zéro

        # Sélectionner automatiquement le premier périphérique disponible
        self.auto_select_device()

    def auto_select_device(self):
        if self.device_list_python:
            # Choisir le premier périphérique disponible
            self.device_id = self.device_list_python[0]
            print(f"Périphérique sélectionné automatiquement: {self.device_id}")
        else:
            raise Exception("Aucun périphérique Kinesis détecté.")

    def connect_motor(self):
        # Vérifier que le périphérique est détecté
        if not self.device_id:
            raise Exception("Aucun périphérique à connecter. Veuillez sélectionner un périphérique.")

        # Connecter au périphérique
        self.motor = KCubeDCServo.CreateKCubeDCServo(self.device_id)
        self.motor.Connect(self.device_id)

    def initialize_motor(self):
        # Initialiser le moteur
        print('Initialisation du moteur...')
        self.motor.LoadMotorConfiguration(self.device_id)
        self.motor.StartPolling(250)
        self.motor.EnableDevice()
        self.motor.Home(60000)  # Temporisation de 60 secondes pour l'opération de homing

    def configure_movement(self, distance_total_mm, temps_total_s):
        # Calculer la vitesse en mm/s
        vitesse_mm_s = 2.0 #distance_total_mm / temps_total_s

        # Convertir en Decimal pour les opérations
        self.distance_total = Decimal(distance_total_mm)
        self.temps_total_s_d = Decimal(temps_total_s)

        # Calculer la vitesse en mm/s
        self.vitesse = Decimal(vitesse_mm_s)

        # Configurer les paramètres de vitesse
        velocity_params = self.motor.GetVelocityParams()
        velocity_params.MaxVelocity = self.vitesse
        self.motor.SetVelocityParams(velocity_params)

    def move_motor(self):
        # Démarrer le mouvement
        print(f'Déplacement de {self.distance_total} mm à une vitesse de {self.vitesse} mm/s')
        self.motor.MoveTo(self.distance_total, Int32(60000))


    def wait_for_completion(self):
        # Attendre la fin du mouvement
        time.sleep(float(self.temps_total_s) + 1.0)  # On attend légèrement plus que le temps total pour être sûr que le mouvement soit terminé

    def disconnect_motor(self):
        # Déconnecter le périphérique
        self.motor.StopPolling()
        self.motor.Disconnect()
        print("Mouvements terminés.")


class DAQ_Move_KDC101(DAQ_Move_base):
    _controller_units = 'degrees'
    _epsilon = 0.05
    is_multiaxes = False
    stage_names = []

    params = [{'title': 'Controller ID:', 'name': 'controller_id', 'type': 'str', 'value': '', 'readonly': True},
              {'title': 'Serial number:', 'name': 'serial_number', 'type': 'list',
               'limits': []},  # Ajustez cette valeur en fonction des numéros de série disponibles
              {'title': 'Backlash:', 'name': 'backlash', 'type': 'float', 'value': 0, },
              ] + comon_parameters_fun(is_multiaxes, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: KCubeDCServoController = None
        self.settings.child('bounds', 'is_bounds').setValue(True)
        self.settings.child('bounds', 'max_bound').setValue(360)
        self.settings.child('bounds', 'min_bound').setValue(0)

    def commit_settings(self, param):
        if param.name() == 'backlash':
            self.controller.backlash = param.value()

    def ini_stage(self, controller=None):
        self.controller = self.ini_stage_init(controller, KCubeDCServoController())

        if self.settings['multiaxes', 'multi_status'] == "Master":
            self.controller.connect_motor()

        info = self.controller.device_id  # Utilisez l'ID du périphérique sélectionné automatiquement
        self.settings.child('controller_id').setValue(info)

        self.controller.backlash = self.settings['backlash']

        initialized = True
        return info, initialized

    def close(self):
        """Close the current instance of Kinesis instrument."""
        if self.controller is not None:
            self.controller.disconnect_motor()

    def stop_motion(self):
        """Stop the current motion."""
        if self.controller is not None:
            self.controller.stop()

    def get_actuator_value(self):
        """Get the current hardware position."""
        pos = self.controller.get_position()
        pos = self.get_position_with_scaling(pos)
        return pos

    def move_abs(self, position):
        """Move to an absolute position."""
        position = self.check_bound(position)
        self.target_position = position
        position = self.set_position_with_scaling(position)

        self.controller.move_motor()

    def move_rel(self, position):
        """Move relative to the current position."""
        position = self.check_bound(self.current_position + position) - self.current_position
        self.target_position = position + self.current_position
        position = self.set_position_relative_with_scaling(position)

        self.controller.move_motor()

    def move_home(self):
        """Move to the home position."""
        self.controller.initialize_motor()
        self.controller.home(callback=self.move_done)



if __name__ == '__main__':
    main(__file__, init=False)