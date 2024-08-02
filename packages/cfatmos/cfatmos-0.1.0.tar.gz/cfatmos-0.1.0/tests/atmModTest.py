from atmosphereModule import Atmosphere

atm = Atmosphere()

air1 = {}
air2 = {"test": 5}

atm.get_atmosphere_data(altitude=22, mach=5)

atm.get_atmosphere_data(air1, altitude=22, mach=5)

atm.get_atmosphere_data(altitude=22, mach=5, container=air2)

assert air1["Pressure"] == air2["Pressure"], print("Test failed")
