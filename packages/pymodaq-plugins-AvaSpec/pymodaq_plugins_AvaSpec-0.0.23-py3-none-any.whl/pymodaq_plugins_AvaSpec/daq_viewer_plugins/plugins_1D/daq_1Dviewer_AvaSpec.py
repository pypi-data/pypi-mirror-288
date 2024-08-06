from ctypes import CDLL, c_int, create_string_buffer, byref, c_ulong, Structure, c_char
from qtpy import QtWidgets
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
import numpy as np
from collections import OrderedDict
from pymodaq.utils.daq_utils import ThreadCommand, getLineInfo
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
import sys
import time
from msl.equipment import EquipmentRecord, ConnectionRecord, Backend

class DAQ_1DViewer_AvaSpec(DAQ_Viewer_base):
    """PyMoDAQ plugin controlling AvaSpec-2048L spectrometers using the Avantes SDK"""

    avaspec_dll_path = 'C:\\AvaSpecX64-DLL_9.14.0.0\\avaspecx64.dll'
    params = comon_parameters + [
        {'title': 'Avantes DLL path:', 'name': 'avaspec_dll_path', 'type': 'browsepath', 'value': avaspec_dll_path},
        {'title': 'N spectrometers:', 'name': 'Nspectrometers', 'type': 'int', 'value': 0, 'default': 0, 'min': 0},
        {'title': 'Spectrometers:', 'name': 'spectrometers', 'type': 'group', 'children': []},
    ]

    def ini_attributes(self):
        self.controller = None
        self.spectro_names = []  # List to store the names of available spectrometers
        self.spectro_id = []  # List to store the IDs of available spectrometers

    def commit_settings(self, param):
        if param.name() == 'avaspec_dll_path':
            self.update_spectrometers_list(param.value())

    def update_spectrometers_list(self, dll_path):
        self.spectro_names = get_spectrometers_list(dll_path)
        print(f"Available spectrometers: {self.spectro_names}")  # Print available spectrometers
        if self.spectro_names:
            self.spectro_id = ['spectro0']  # Only the first spectrometer ID

            self.settings.child('Nspectrometers').setValue(1)
            self.settings.child('spectrometers').clear()
            self.settings.child('spectrometers').addChild({
                'title': self.spectro_names[0],
                'name': 'spectro0',
                'type': 'group',
                'children': [
                    {'title': 'grab spectrum:', 'name': 'grab', 'type': 'bool', 'value': True},
                    {'title': 'Exposure time (ms):', 'name': 'exposure_time', 'type': 'int', 'value': 5, 'min': 1,
                     'max': 10000},
                ]
            })

    def ini_detector(self, controller=None):
        if self.settings['controller_status'] == "Slave":
            if controller is None:
                raise Exception('No controller has been defined externally while this axe is a slave one')
            else:
                self.controller = controller
        else:
            self.initialize_controller(self.settings.child('avaspec_dll_path').value())
            if self.controller is None:
                return '', False

            try:
                num_pixels = self.controller.get_num_pixels()
                wavelengths = self.controller.get_lambda()
                data_init = DataToExport('Spectro')
                data_init.append(DataFromPlugins(name=self.spectro_names[0], data=[np.zeros(num_pixels)], dim='Data1D',
                                                 axes=[Axis(data=wavelengths, label='Wavelength', units='nm')]))

                self.dte_signal_temp.emit(data_init)
            except Exception as e:
                print(f"Failed to initialize spectrometer: {e}")
                return '', False

        initialized = True
        info = 'Detector initialized successfully'
        return info, initialized

    def initialize_controller(self, dll_path):
        try:
            # Check if the spectrometer names list is empty
            if not self.spectro_names:
                # If empty, retrieve the list of spectrometers
                self.spectro_names = get_spectrometers_list(dll_path)
                print(f"Available spectrometers: {self.spectro_names}")

            # Proceed only if there are spectrometers available
            if self.spectro_names:
                serial_number = self.spectro_names[0]  # Use the first detected spectrometer for initialization
                print(f"Attempting to connect to AvaSpec-2048L with serial number: {serial_number}")

                # Create a connection record
                record = EquipmentRecord(
                    manufacturer='Avantes',
                    model='AvaSpec-2048L',
                    serial=serial_number,
                    connection=ConnectionRecord(
                        address=f'SDK::{dll_path}',
                        backend=Backend.MSL,
                    )
                )
                self.controller = record.connect()
                print(f'Connected to AvaSpec-2048L with serial number: {serial_number}')
            else:
                print("No spectrometers found")
                self.controller = None

        except Exception as e:
            print(f"Failed to connect to AvaSpec-2048L: {e}")
            self.controller = None

    def get_xaxis(self, ind_spectro):
        try:
            wavelengths = self.controller.get_lambda()
            return wavelengths
        except Exception as e:
            print(f"Failed to get wavelengths for spectrometer {ind_spectro}: {e}")
            return np.array([])

    def close(self):
        if self.controller is not None:
            self.controller.disconnect()

    def grab_data(self, Naverage=1, **kwargs):
        print("Data emitted to signal")

    def stop(self):
        # No specific stop function provided in example script, assuming stopAveraging is not required for AvaSpec
        pass


def get_spectrometers_list(dll_path):
    dll = CDLL(dll_path)

    try:
        # Initialiser le SDK pour USB uniquement
        print("Initializing SDK...")
        result = dll.AVS_Init(c_int(0))  # 0 pour utiliser le port USB uniquement
        if result <= 0:
            print(f"Error initializing SDK: {result}")
            return []
        print("SDK initialized successfully")

        # Mettre à jour les périphériques USB
        print("Updating USB devices...")
        usb_result = dll.AVS_UpdateUSBDevices()
        print(f"USB devices count: {usb_result}")

        # Déterminer la taille du buffer nécessaire pour obtenir la liste des périphériques
        print("Determining buffer size...")
        list_size = c_ulong(0)
        result = dll.AVS_GetList(c_ulong(0), byref(list_size), None)
        print(f"Result of AVS_GetList for buffer size determination: {result}, List Size: {list_size.value}")

        if result != 0:
            # Allouer le buffer pour la liste des périphériques
            buffer_size = list_size.value
            print(f"Allocating buffer of size: {buffer_size}")
            buffer = create_string_buffer(buffer_size)

            # Obtenir la liste des périphériques
            print("Getting the list of devices...")
            result = dll.AVS_GetList(c_ulong(buffer_size), byref(list_size), buffer)
            print(f"Result of AVS_GetList for device list retrieval: {result}")

            if result != 0:
                # Traiter la liste des périphériques
                raw_data = buffer.raw
                print("Raw buffer data:", raw_data)

                # Extraire les numéros de série
                spectrometers = []
                index = 0
                while index < len(raw_data):
                    # Extraire le numéro de série
                    end_index = raw_data.find(b'U1', index)
                    if end_index == -1:
                        break
                    serial_number = raw_data[index:end_index + 2].decode('utf-8', errors='ignore').strip('\x00')
                    if serial_number:
                        print(f"Spectrometer found with Serial Number: {serial_number}")
                        spectrometers.append(serial_number)
                    index = end_index + 2  # Passer à l'élément suivant

                return spectrometers
            else:
                print("No devices found or error in getting the device list.")
        else:
            print("Error in determining buffer size.")

    except Exception as e:
        print(f"Exception occurred: {e}")

    finally:
        # Désactiver le SDK
        print("Deinitializing SDK...")
        dll.AVS_Done()
        print("SDK deinitialized")

    return []


if __name__ == '__main__':
    main(__file__)
