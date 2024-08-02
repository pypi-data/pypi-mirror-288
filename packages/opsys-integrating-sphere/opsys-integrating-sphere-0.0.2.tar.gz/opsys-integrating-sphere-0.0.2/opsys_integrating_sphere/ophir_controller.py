import win32com.client
import time
from .i_sphere_abstract import ISphereAbstract


TIMEOUT = 0.1


class OphirController(ISphereAbstract):
    """
    Ophir Integrating Sphere Controller
    """

    def __init__(self, wavelength):
        """
        Initialize parameters

        Args:
            wavelength (int): laser wavelength 905/940 (nm)

        Raises:
            ValueError: in case invalid wavelength value passed
        """
        self._ophir_conn = None
        self._ophir_port = None
        
        if wavelength == 940:
            self.wavelength = 2
            
        elif wavelength == 905:
            self.wavelength = 3
            
        else:
            raise ValueError("Invalid wavelength value received")

    def scan_ports(self):
        """
        Check for device connection

        Returns:
            bool: True if the device connected, else False
        """
        device_list = self._ophir_conn.ScanUSB()
        
        for device in device_list:
            self._ophir_port = self._ophir_conn.OpenUSBDevice(device)
            
        return self._ophir_conn.IsSensorExists(self._ophir_port, 0)

    def connect(self):
        """
        Connect to integrating sphere
        """
        self.disconnect()
        self._ophir_conn = win32com.client.Dispatch(
            "OphirLMMeasurement.CoLMMeasurement")
        
        is_connected = self.scan_ports()  # check if connected
        
        if is_connected:
            print("Ophir connected successfully")
        else:
            print("Ophir connection error")

    def disconnect(self):
        """
        Disconnect from integrating sphere
        """
        self._ophir_conn.StopAllStreams()
        self._ophir_conn.CloseAll()
        print("Ophir disconnected")

    def get_optical_power(self):
        """
        Measure optical power

        Returns:
            float: measured optical power value 
        """
        self._ophir_conn.SetWavelength(self._ophir_port, 0, self.wavelength)
        time.sleep(TIMEOUT)
        
        print("Start Optical Power Measurements")
        
        self._ophir_conn.Write(self._ophir_port, "sp")
        measured_value = self._ophir_conn.Read(self._ophir_port)
        measured_value = float(measured_value.replace("*", ""))
        
        return measured_value
