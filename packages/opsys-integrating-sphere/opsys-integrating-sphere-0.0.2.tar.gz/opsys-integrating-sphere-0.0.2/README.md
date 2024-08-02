# README #

This README would normally document whatever steps are necessary to get your application up and running.

### What is this repository for? ###

* This repository is a part of opsys automation infrastructure
* This repository is integrating sphere controller implementation of Artifex/Ophir devices 

### How do I get set up? ###

* pip install opsys-integrating-sphere

### Unit Testing

* python -m unittest -v

### Usage Example
```
from opsys_integrating_sphere.i_sphere_controller import ISphereController

i_sphere = ISphereController(i_sphere_type='Artifex', wavelength=940)

i_sphere.connect()
i_sphere.get_optical_power()
i_sphere.disconnect()
```