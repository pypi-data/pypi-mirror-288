**INFO** \
The Atmosphere module is a simple module that can be used by itself to quickly provide air
properties or can be incorporated into larger Python scripts when air properties are needed for
other calculations.

All of the functionality of the module is contained within one class, Atmosphere. Usage for
this class is outlined below.

**USAGE** \
Everything you will ever need out of the module is given through the _get_atmosphere_data_ method.
Depending on your inputs the module can work in one of two modes, either 'Atmosphere Model' mode
or 'Ideal Gas Model' mode. See below for details.

Additionally, the module can either print your result or return for further use. To have the results
returned, pass a dictionary as the first argument and it will come back **updated** with your air properties

For Atmosphere Model Mode provide one of the following inputs - Altitude - Pressure - Density

For Ideal Gas Mode provide two inputs such as -- Pressure, Temperature -- Density, Temperature

(Optional Inputs) Velocity or Mach number can be given as optional inputs in either mode. When
one of these values are given the output list contains the other along with
Reynolds number per unit length.
