from qtpy import QtWidgets
from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
import numpy as np
from collections import OrderedDict
from pymodaq.utils.daq_utils import ThreadCommand, getLineInfo
from pymodaq.utils.data import DataFromPlugins, Axis, DataToExport
import ctypes

# Importation dynamique des fonctions AvaSpec depuis le DLL
ava_dll_path = 'C:\\AvaSpecX64-DLL_9.14.0.0\\avaspecx64.dll'
ava_dll = ctypes.CDLL(ava_dll_path)

# Déclaration des prototypes des fonctions AvaSpec
ava_dll.AVS_Init.argtypes = []
ava_dll.AVS_Init.restype = ctypes.c_int
ava_dll.AVS_GetNrOfDevices.argtypes = []
ava_dll.AVS_GetNrOfDevices.restype = ctypes.c_int
ava_dll.AVS_GetDeviceType.argtypes = [ctypes.c_int, ctypes.c_char_p]
ava_dll.AVS_GetDeviceType.restype = ctypes.c_int
ava_dll.AVS_GetDetectorName.argtypes = [ctypes.c_int, ctypes.c_char_p]
ava_dll.AVS_GetDetectorName.restype = ctypes.c_int
ava_dll.AVS_GetLambda.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
ava_dll.AVS_GetLambda.restype = ctypes.c_int
ava_dll.AVS_Measure.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
ava_dll.AVS_Measure.restype = ctypes.c_int

class DAQ_1DViewer_AvaSpec(DAQ_Viewer_base):
    """PyMoDAQ plugin controlling spectrometers using the Avantes AvaSpec library.
    This plugin enables the discovery of any connected USB spectrometers and can control them in parallel.
    It extracts the calibrated wavelength and will export data that will be plotted with respect to this wavelengths vector.
    """
    ava_dll_path = ava_dll_path

    params = comon_parameters + [
        {'title': 'AvaSpec DLL path:', 'name': 'avaspec_dll_path', 'type': 'browsepath', 'value': ava_dll_path},
        {'title': 'N spectrometers:', 'name': 'Nspectrometers', 'type': 'int', 'value': 0, 'default': 0, 'min': 0},
        {'title': 'Spectrometers:', 'name': 'spectrometers', 'type': 'group', 'children': []},
    ]

    hardware_averaging = True

    def ini_attributes(self):
        self.controller = None
        self.spectro_names = []
        self.spectro_id = []

    def commit_settings(self, param):
        if param.name() == 'avaspec_dll_path':
            self.load_dll(param.value())

    def load_dll(self, dll_path):
        global ava_dll
        ava_dll = ctypes.CDLL(dll_path)
        # Re-déclaration des prototypes des fonctions après rechargement du DLL
        ava_dll.AVS_Init.argtypes = []
        ava_dll.AVS_Init.restype = ctypes.c_int
        ava_dll.AVS_GetNrOfDevices.argtypes = []
        ava_dll.AVS_GetNrOfDevices.restype = ctypes.c_int
        ava_dll.AVS_GetDeviceType.argtypes = [ctypes.c_int, ctypes.c_char_p]
        ava_dll.AVS_GetDeviceType.restype = ctypes.c_int
        ava_dll.AVS_GetDetectorName.argtypes = [ctypes.c_int, ctypes.c_char_p]
        ava_dll.AVS_GetDetectorName.restype = ctypes.c_int
        ava_dll.AVS_GetLambda.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        ava_dll.AVS_GetLambda.restype = ctypes.c_int
        ava_dll.AVS_Measure.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_double)]
        ava_dll.AVS_Measure.restype = ctypes.c_int

    def ini_detector(self, controller=None):
        if self.settings['controller_status'] == "Slave":
            if controller is None:
                raise Exception('No controller has been defined externally while this axe is a slave one')
            else:
                self.controller = controller
        else:  # Master stage
            try:
                # Initialisation du DLL
                ava_dll.AVS_Init()
                print("AvaSpec DLL initialized")
            except Exception as e:
                print(f"Failed to initialize AvaSpec DLL: {e}")
                return '', False

            try:
                N = ava_dll.AVS_GetNrOfDevices()
                print(f"Number of spectrometers opened: {N}")
                self.settings.child('Nspectrometers').setValue(N)
            except Exception as e:
                print(f"Failed to open spectrometers: {e}")
                return '', False

            self.spectro_names = []
            self.spectro_id = []
            data_init = DataToExport('Spectro')

            for ind_spectro in range(N):
                try:
                    # Récupérer le type du spectromètre
                    type_buffer = ctypes.create_string_buffer(256)
                    result = ava_dll.AVS_GetDeviceType(ind_spectro, type_buffer)
                    if result != 0:
                        raise Exception(f"Failed to get type for spectrometer {ind_spectro}")
                    device_type = type_buffer.value.decode('utf-8')
                    print(f"Spectrometer {ind_spectro} type: {device_type}")

                    # Récupérer le nom du spectromètre
                    name_buffer = ctypes.create_string_buffer(256)
                    result = ava_dll.AVS_GetDetectorName(ind_spectro, name_buffer)
                    if result != 0:
                        raise Exception(f"Failed to get name for spectrometer {ind_spectro}")
                    name = name_buffer.value.decode('utf-8')
                    print(f"Spectrometer {ind_spectro} name: {name}")
                    self.spectro_names.append(name)
                    self.spectro_id.append(f'spectro{ind_spectro}')

                    wavelengths = self.get_xaxis(ind_spectro)
                    data_init.append(DataFromPlugins(name=name, data=[np.zeros_like(wavelengths)], dim='Data1D',
                                                     axes=[Axis(data=wavelengths, label='Wavelength', units='nm')]
                                                     ))

                    self.settings.child('spectrometers').addChild(
                        {'title': name, 'name': f'spectro{ind_spectro}', 'type': 'group', 'children': [
                            {'title': 'grab spectrum:', 'name': 'grab', 'type': 'bool', 'value': True},
                            # Note: The AvaSpec DLL does not provide direct methods for exposure time settings.
                            # This would need to be adapted based on your specific hardware capabilities.
                        ]}
                    )

                    QtWidgets.QApplication.processEvents()
                except Exception as e:
                    print(f"Error initializing spectrometer {ind_spectro}: {e}")

            if N == 0:
                raise Exception('No detected hardware')

            self.dte_signal_temp.emit(data_init)

        initialized = True
        info = 'Detector initialized successfully'
        print(info)
        return info, initialized

    def get_xaxis(self, ind_spectro):
        try:
            wavelengths_chelou = np.zeros(2048)  # Example size, replace with actual size if known
            result = ava_dll.AVS_GetWavelengths(ind_spectro, wavelengths_chelou)
            if result != 0:
                print(f"Failed to get wavelengths for spectrometer {ind_spectro}")
                return np.array([])
            return np.array(wavelengths_chelou)
        except Exception as e:
            print(f"Failed to get wavelengths for spectrometer {ind_spectro}: {e}")
            return np.array([])

    def close(self):
        if self.controller is not None:
            # Assuming AvaSpec DLL does not provide a close method.
            pass

    def grab_data(self, Naverage=1, **kwargs):
        try:
            dte = DataToExport('Spectro')
            for ind_spectro in range(len(self.spectro_names)):
                if self.settings.child('spectrometers', f'spectro{ind_spectro}', 'grab').value():
                    data_chelou = np.zeros(2048)  # Example size, replace with actual size if known
                    result = ava_dll.AVS_Measure(ind_spectro, data_chelou)
                    if result != 0:
                        print(f"Failed to grab data for spectrometer {ind_spectro}")
                        continue
                    data_array = np.array(data_chelou)
                    dte.append(DataFromPlugins(name=self.spectro_names[ind_spectro], data=[data_array], dim='Data1D'))
                    QtWidgets.QApplication.processEvents()

            self.dte_signal.emit(dte)
        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status', [getLineInfo() + str(e), "red"]))

if __name__ == '__main__':
    main(DAQ_1DViewer_AvaSpec)
