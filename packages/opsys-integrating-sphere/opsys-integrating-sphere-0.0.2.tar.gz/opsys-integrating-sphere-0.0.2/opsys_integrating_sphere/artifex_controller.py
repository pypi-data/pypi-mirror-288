import serial
from serial import SerialException
import re
from .i_sphere_abstract import ISphereAbstract

# avoild COMs detection at deployment
try:
    import serial.tools.list_ports
except Exception as e:
    print(e)


BAUDRATE = 115200
TIMEOUT = 5
P_MULTI = 100000


class ArtifexController(ISphereAbstract):
    """
    OPM150 Artifex Integrating Sphere Controller
    """

    def __init__(self):
        """
        Initialize parameters
        """
        self._artifex_conn = None
        self._artifex_port = None

    def scan_ports(self):
        """
        Check for valid COM ports

        Raises:
            SerialException: No valid ports detected
        """
        ports = serial.tools.list_ports.comports()
        
        for port, desc, _ in sorted(ports):
            if "OPM150" in desc:
                self._artifex_port = port
                
        if self._artifex_port is None:
            raise SerialException('No valid COM port detected')

    def connect(self):
        """
        Connect to integrating sphere
        """
        self.scan_ports()  # get port
        self._artifex_conn = serial.Serial(
            self._artifex_port, BAUDRATE, timeout=TIMEOUT, parity=serial.PARITY_NONE)
        
        if self._artifex_conn.isOpen() == True:
            print("Artifex connected successfully")
        else:
            print("Artifex connection error")

    def disconnect(self):
        """
        Disconnect from integrating sphere
        """
        self._artifex_conn.close()
        print("Artifex disconnected")

    def init(self):
        """
        Initialize integrating sphere
        """
        for msg in ["$U", "V?", "B?", "$F", "$I", "V2", "V3", "V4", "V5"]:
            self._artifex_conn.write(msg.encode() + '\n'.encode())
            
        print("Artifex init done")

    def get_optical_power(self):
        """
        Measure optical power

        Returns:
            float: measured optical power value 
        """
        optical_power = "0"
        pulse_length = "$L0920"
        
        print("Start Optical Power Measurements")
        
        self._artifex_conn.write("$E".encode() + '\n'.encode())
        measured_value = self._artifex_conn.readline().decode().strip()
        
        for i in measured_value:
            if i.isnumeric():
                measured_parrs = measured_parrs + i
                
        self._artifex_conn.write(pulse_length.encode() + '\n'.encode())
        cal_val = self._artifex_conn.readline().decode().strip().replace(",", ".")
        cal_val = re.findall("\d+\.\d+", cal_val)
        cal_val = cal_val[0]
        optical_power = (P_MULTI * (float(measured_parrs) /
                        float(cal_val))) / 1000000000
        
        return optical_power
