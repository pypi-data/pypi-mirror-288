import unittest
from unittest.mock import patch, MagicMock
from opsys_integrating_sphere.i_sphere_controller import ISphereController


I_SPHERE_TYPE = 'Artifex'


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass
    
    @ patch.object(ISphereController, 'connect')
    def test_connect(self, i_sphere_mock: MagicMock):
        i_sphere = ISphereController(i_sphere_type=I_SPHERE_TYPE, wavelength=940)
        i_sphere.connect()
        i_sphere_mock.assert_called_once_with()
        
    @ patch.object(ISphereController, 'disconnect')
    def test_disconnect(self, i_sphere_mock: MagicMock):
        i_sphere = ISphereController(i_sphere_type=I_SPHERE_TYPE, wavelength=940)
        i_sphere.disconnect()
        i_sphere_mock.assert_called_once_with()
   
    @ patch.object(ISphereController, 'get_optical_power')
    def test_get_optical_power(self, i_sphere_mock: MagicMock):
        i_sphere = ISphereController(i_sphere_type=I_SPHERE_TYPE, wavelength=940)
        i_sphere.get_optical_power()
        i_sphere_mock.assert_called_once_with()
        
    @ patch.object(ISphereController, 'connect')
    def test_connect_2(self, i_sphere_mock: MagicMock):
        i_sphere = ISphereController(i_sphere_type=I_SPHERE_TYPE, wavelength=905)
        i_sphere.connect()
        i_sphere_mock.assert_called_once_with()
        
    @ patch.object(ISphereController, 'disconnect')
    def test_disconnect_2(self, i_sphere_mock: MagicMock):
        i_sphere = ISphereController(i_sphere_type=I_SPHERE_TYPE, wavelength=905)
        i_sphere.disconnect()
        i_sphere_mock.assert_called_once_with()
   
    @ patch.object(ISphereController, 'get_optical_power')
    def test_get_optical_power_2(self, i_sphere_mock: MagicMock):
        i_sphere = ISphereController(i_sphere_type=I_SPHERE_TYPE, wavelength=905)
        i_sphere.get_optical_power()
        i_sphere_mock.assert_called_once_with()
    

if __name__ == '__main__':
    unittest.main()
