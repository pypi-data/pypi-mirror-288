from .i_sphere_abstract import ISphereAbstract


class ISphereController(ISphereAbstract):
    """
    Integrating Sphere controller class
    """

    def __init__(self, i_sphere_type, wavelength):
        """
        Initialize parameters

        Args:
            i_sphere_type (str): integrating sphere type - Ophir/Artifex
            wavelength (int): laser wavelength in nm

        Raises:
            ValueError: in case wrong device type passed
        """
        self.i_sphere_type = i_sphere_type
        
        if self.i_sphere_type.upper() == "OPHIR":
            from .ophir_controller import OphirController

            self._i_sphere = OphirController(wavelength=wavelength)

        elif self.i_sphere_type.upper() == "ARTIFEX":
            from .artifex_controller import ArtifexController

            self._i_sphere = ArtifexController()
        else:
            raise ValueError("Can't find integrating sphere type")

    def connect(self):
        """
        Connect to integrating sphere
        """
        self._i_sphere.connect()

    def disconnect(self):
        """
        Disconnect from integrating sphere
        """
        self._i_sphere.disconnect()

    def get_optical_power(self):
        """
        Measure optical power

        Returns:
            float: measured optical power value 
        """
        if self.i_sphere_type == "Artifex":
            self._i_sphere.init()
            
        return self._i_sphere.get_optical_power()
