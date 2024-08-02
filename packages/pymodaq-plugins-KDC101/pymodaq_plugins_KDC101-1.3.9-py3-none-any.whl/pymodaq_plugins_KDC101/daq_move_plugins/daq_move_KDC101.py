from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun, main)
import clr
import sys
import time
from System import Decimal, Action, UInt64, UInt32

# Ajouter le chemin d'accès aux DLLs Kinesis
kinesis_path = 'C:\\Program Files\\Thorlabs\\Kinesis'
sys.path.append(kinesis_path)

clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.GenericMotorCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.DCServoCLI")

import Thorlabs.MotionControl.KCube.DCServoCLI as DCServo
import Thorlabs.MotionControl.DeviceManagerCLI as Device
import Thorlabs.MotionControl.GenericMotorCLI as Generic

# Construire la liste des périphériques disponibles
Device.DeviceManagerCLI.BuildDeviceList()

# Préfixe correct pour les périphériques KCube DCServo
device_prefix = DCServo.KCubeDCServo.DevicePrefix  # Assurez-vous d'utiliser le bon préfixe

# Obtenez la liste des périphériques en utilisant le préfixe approprié
device_list = Device.DeviceManagerCLI.GetDeviceList(device_prefix)

# Sélectionnez seulement le premier périphérique si disponible
serialnumbers_Kcube = [str(device_list[0])] if device_list else []

class Kinesis:

    def __init__(self):
        self._device = None

    def connect(self, serial: str):
        if self._device:
            self._device.Connect(serial)
            self._device.WaitForSettingsInitialized(5000)
            self._device.StartPolling(250)
        else:
            raise ValueError('Device not initialized')

    def close(self):
        """
        Close the current instance of Kinesis instrument.
        """
        if self._device:
            self._device.StopPolling()
            self._device.Disconnect()
            self._device.Dispose()
            self._device = None

    @property
    def name(self) -> str:
        if self._device:
            return self._device.GetDeviceInfo().Name
        return ''

    @property
    def backlash(self):
        if self._device:
            return Decimal.ToDouble(self._device.GetBacklash())
        return 0.0

    @backlash.setter
    def backlash(self, backlash: float):
        if self._device:
            self._device.SetBacklash(Decimal(backlash))

    def stop(self):
        if self._device:
            self._device.Stop(0)

    def move_abs(self, position: float, callback=None):
        if self._device:
            if callback is not None:
                callback = Action[UInt64](callback)
            else:
                callback = Action[UInt64](lambda x: None)  # Default empty callback
            self._device.MoveTo(Decimal(position), callback)

    def move_rel(self, position: float, callback=None):
        if self._device:
            if callback is not None:
                callback = Action[UInt64](callback)
            else:
                callback = Action[UInt64](lambda x: None)  # Default empty callback
            self._device.MoveRelative(Generic.MotorDirection.Forward, Decimal(position), callback)

    def home(self, callback=None):
        if self._device:
            if callback is not None:
                callback = Action[UInt64](callback)
            else:
                callback = Action[UInt64](lambda x: None)  # Default empty callback
            self._device.Home(callback)

    def get_position(self):
        raise NotImplementedError

class KDC101(Kinesis):
    def __init__(self):
        super().__init__()
        self._device: DCServo.KCubeDCServo = None

    def connect(self, serial: str):
        if serial in serialnumbers_Kcube:
            self._device = DCServo.KCubeDCServo.CreateKCubeDCServo(serial)
            super().connect(serial)
            if not self._device.IsSettingsInitialized():
                raise Exception("Device not initialized correctly")
        else:
            raise ValueError('Invalid Serial Number')

    def move_abs(self, position: float, callback=None):
        if self._device:
            self._device.SetPosition(UInt32(position), 0)

    def get_position(self):
        if self._device:
            return Decimal.ToDouble(self._device.GetPosition())

class DAQ_Move_KDC101(DAQ_Move_base):
    _controller_units = 'degrees'
    _epsilon = 0.05
    is_multiaxes = False
    stage_names = []

    params = [{'title': 'Controller ID:', 'name': 'controller_id', 'type': 'str', 'value': '', 'readonly': True},
              {'title': 'Serial number:', 'name': 'serial_number', 'type': 'list', 'limits': serialnumbers_Kcube},
              ] + comon_parameters_fun(is_multiaxes, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: KDC101 = None
        self.settings.child('bounds', 'is_bounds').setValue(True)
        self.settings.child('bounds', 'max_bound').setValue(1)
        self.settings.child('bounds', 'min_bound').setValue(0)

    def commit_settings(self, param):
        if param.name() == 'backlash':
            self.controller.backlash = param.value()

    def ini_stage(self, controller=None):
        self.controller = self.ini_stage_init(controller, KDC101())

        if self.settings['multiaxes', 'multi_status'] == "Master":
            self.controller.connect(self.settings['serial_number'])

        info = self.controller.name
        self.settings.child('controller_id').setValue(info)

        initialized = True
        return info, initialized

    def close(self):
        if self.controller:
            self.controller.close()

    def stop_motion(self):
        if self.controller:
            self.controller.stop()

    def get_actuator_value(self):
        if self.controller:
            pos = self.controller.get_position()
            pos = self.get_position_with_scaling(pos)
            return pos
        return 0.0

    def move_abs(self, position):
        position = self.check_bound(position)
        self.target_position = position
        position = self.set_position_with_scaling(position)

        if self.controller:
            self.controller.move_abs(position)

    def move_rel(self, position):
        position = self.check_bound(self.current_position + position) - self.current_position
        self.target_position = position + self.current_position
        position = self.set_position_relative_with_scaling(position)

        if self.controller:
            self.controller.move_rel(position)

    def move_home(self):
        if self.controller:
            self.controller.home(callback=self.move_done)

if __name__ == '__main__':
    main(__file__, init=False)
