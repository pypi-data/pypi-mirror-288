from typing import overload
from importlib import resources

import numpy as np
import pandas as pd


class Atmosphere:
    def __init__(self):
        self.__binFormat = [
            ("Altitude[km]", "f8"),
            ("Temperature[K]", "f8"),
            ("Pressure[Pa]", "f8"),
            ("Density[kg/m^3]", "f8"),
            ("SoS[m/s]", "f8"),
            ("Viscosity[Pa.s]", "f8"),
        ]

        dataPath = resources.files("cfatmos") / "data/tabulated_data.bin"
        dataPath = str(dataPath)
        self.__data = np.fromfile(dataPath, dtype=self.__binFormat)
        self.__data = pd.DataFrame(self.__data)

        self.__namedQuantitiesToDataMap = {
            "Altitude": "Altitude[km]",
            "Pressure": "Pressure[Pa]",
            "Density": "Density[kg/m^3]",
            "Temperature": "Temperature[K]",
            "Velocity": "Velocity[m/s]",
            "Mach Number": "Mach",
            "Speed of Sound": "SoS[m/s]",
            "Viscosity": "Viscosity[Pa.s]",
            "Reynolds No.": "Reynolds Number[1/m]",
        }

        self.__namedQuantities = [
            "Altitude",
            "Pressure",
            "Density",
            "Temperature",
            "Velocity",
            "Mach Number",
            "Speed of Sound",
            "Viscosity",
            "Reynolds No.",
        ]

        self.__quantitiesDict = {
            "Altitude": np.nan,
            "Pressure": np.nan,
            "Density": np.nan,
            "Temperature": np.nan,
            "Velocity": np.nan,
            "Mach Number": np.nan,
            "Speed of Sound": np.nan,
            "Viscosity": np.nan,
            "Reynolds No.": np.nan,
        }

        self.__excludeList = ["Velocity", "Mach Number", "Reynolds No."]

        self.__defaultValues = {
            "Altitude": 0,
            "Pressure": 101325,
            "Density": 1.225,
            "Temperature": 288.15,
            "Velocity": np.nan,
            "Mach Number": np.nan,
        }

        self.__primaryList = ["Altitude", "Pressure", "Density"]

        self.__secondaryList = ["Temperature"]

    def __str__(self):
        # Create formatted string for output
        printStr = f"Altitude      : {self.__quantitiesDict['Altitude']:.2f} km / {self.__quantitiesDict['Altitude']*3.28084:.5f} kft\n"
        printStr += f"Pressure      : {self.__quantitiesDict['Pressure']:.2f} Pa\n"
        printStr += f"Density       : {self.__quantitiesDict['Density']:.2f} kg/m^3\n"
        printStr += f"Temperature   : {self.__quantitiesDict['Temperature']:.2f} K\n"
        printStr += f"Velocity      : {self.__quantitiesDict['Velocity']:.2f} m/s\n"
        printStr += f"Mach Number   : {self.__quantitiesDict['Mach Number']:.2f}\n"
        printStr += (
            f"Speed of Sound: {self.__quantitiesDict['Speed of Sound']:.2f} m/s\n"
        )
        printStr += f"Viscosity     : {self.__quantitiesDict['Viscosity']:.2e} Pa.s\n"
        printStr += f"Reynolds No.  : {self.__quantitiesDict['Reynolds No.']:.2f} 1/m\n"

        return printStr

    def __repr__(self):
        return self.__str__()

    def help(self):
        print(self.get_atmosphere_data.__doc__)
        return None

    @overload
    def get_atmosphere_data(
        self, container: None | dict[str, float] = ..., **kwargs
    ) -> None: ...

    @overload
    def get_atmosphere_data(self, **kwargs) -> str: ...

    def get_atmosphere_data(self, container=None, **kwargs) -> None | str:
        """
        INPUTS: (container: dict, **kwargs)
        container: dict (optional) - If provided, the output will be stored in the container.
        kwargs: keyword arguments - The input values to calculate atmosphere data.

        OUTPUTS: If container is provided, the output is stored in the container.
        Otherwise, the output is printed to the console.

        INFO:
        This calculator has two modes, 'Atmosphere Model Mode' and 'Ideal Gas Mode'.
        To return values calculated from the 1976 Standard Atmosphere Model give one of the following inputs
            - Altitude
            - Pressure
            - Density
        ------------------------------
            (Optional Inputs)
            - Velocity
            - Mach Number

        To return values calculated using the Ideal Gas Law, give two of the following inputs
            - Pressure and Temperature
            - Density and Temperature
        ------------------------------
            (Optional Inputs)
            - Velocity
            - Mach Number


        Values are passed as keyword arguments. The output is determined by whether or not a
        dictionary is passed (either the first argument or by keyword 'container').
        If a dictionary is passed, the output is stored in the dictionary.
        If no dictionary is passed, the output is printed.

        --------------------------------------------------------------------------------

        EXAMPLES:
        1. Given Altitude: 22 km, Mach Number: 5.0
            Input:
                atm.get_atmosphere_data(altitude=22, mach=5.0)
            Output:
                Altitude      : 22 km / 72.17848 kft
                Pressure      : 3999.79021987796 Pa
                Density       : 0.0637273460752437 kg/m^3
                Temperature   : 218.65 K
                Velocity      : 1482.141978944665 m/s
                Mach Number   : 5.0
                Speed of Sound: 296.428395788933 m/s
                Viscosity     : 1.44356649242e-05 Pa.s
                Reynolds No.  : 6543029.040976971 1/m


        2. Given Density: 0.1 kg/m^3, Temperature: 220 K
            Input:
                atm.get_atmosphere_data(density=0.1, temperature=220)
            Output:
                Altitude      : 19.191900238569218 km / 62.96555397870743 kft
                Pressure      : 6315.1 Pa
                Density       : 0.1 kg/m^3
                Temperature   : 220 K
                Velocity      : None m/s
                Mach Number   : None
                Speed of Sound: 297.34054550296366 m/s
                Viscosity     : 1.4399635754968554e-05 Pa.s
                Reynolds No.  : None 1/m

        """

        self.__clearData()

        formattedArgs = self.__format_input(kwargs)

        primary: str = ""
        secondary: str = ""
        for key in formattedArgs.keys():
            self.__quantitiesDict[key] = formattedArgs.get(
                key, self.__defaultValues[key]
            )
            if key in self.__primaryList:
                primary = key
            if key in self.__secondaryList:
                secondary = key

        if secondary == "":
            self.__boundsCheck(formattedArgs)

        self.__atmosphere_lookup(primary, secondary)

        if "Velocity" in formattedArgs:
            self.__quantitiesDict["Mach Number"] = (
                self.__quantitiesDict["Velocity"]
                / self.__quantitiesDict["Speed of Sound"]
            )

        elif "Mach Number" in formattedArgs:
            self.__quantitiesDict["Velocity"] = (
                self.__quantitiesDict["Mach Number"]
                * self.__quantitiesDict["Speed of Sound"]
            )

        if self.__quantitiesDict["Velocity"] is not np.nan:
            self.__quantitiesDict["Reynolds No."] = (
                self.__quantitiesDict["Density"] * self.__quantitiesDict["Velocity"]
            ) / self.__quantitiesDict["Viscosity"]

        if container is not None:
            container.update(self.__quantitiesDict)
            return None

        return print(self)

    def __clearData(self):

        for key in self.__quantitiesDict.keys():
            self.__quantitiesDict[key] = np.nan

        return None

    def __format_input(self, kwargs) -> dict:
        # format inputs so we can accept any case or a few different variants of words

        formattedArgs = {}

        for key in kwargs.keys():
            if key.lower() in self.__namedQuantities:
                formattedArgs[key] = kwargs[key]
            elif key.lower() == "mach number":
                formattedArgs["Mach Number"] = kwargs[key]
            elif key.lower() == "mach":
                formattedArgs["Mach Number"] = kwargs[key]
            elif key.lower() == "velocity":
                formattedArgs["Velocity"] = kwargs[key]
            elif key.lower() == "temperature":
                formattedArgs["Temperature"] = kwargs[key]
            elif key.lower() == "pressure":
                formattedArgs["Pressure"] = kwargs[key]
            elif key.lower() == "density":
                formattedArgs["Density"] = kwargs[key]
            elif key.lower() == "altitude":
                formattedArgs["Altitude"] = kwargs[key]

        return formattedArgs

    def __boundsCheck(self, formattedArgs) -> None:

        for key in formattedArgs.keys():
            dataKey = self.__namedQuantitiesToDataMap[key]
            if key in self.__excludeList:
                continue
            if formattedArgs[key] < self.__data[dataKey].min():
                raise ValueError(
                    "{} is below the minimum value of {:.2f}".format(
                        key, self.__data[dataKey].min()
                    )
                )
            elif formattedArgs[key] > self.__data[dataKey].max():
                raise ValueError(
                    "{} is above the maximum value of {:.2f}".format(
                        key, self.__data[dataKey].max()
                    )
                )

    def __atmosphere_lookup(self, driver: str, secondary: str = "") -> None:

        if secondary != "":
            self.__model_ideal_gas_lookup(driver)
        else:
            self.__model_only_lookup(driver)

    def __model_ideal_gas_lookup(self, driver: str) -> None:

        dataKey = self.__namedQuantitiesToDataMap[driver]
        self.__data.index = self.__data[dataKey]

        try:
            self.__quantitiesDict["Altitude"] = self.__data.loc[
                self.__quantitiesDict[driver], "Altitude[km]"
            ]
        except KeyError:
            x1 = self.__data[dataKey][
                self.__data[dataKey] < self.__quantitiesDict[driver]
            ].max()
            x2 = self.__data[dataKey][
                self.__data[dataKey] > self.__quantitiesDict[driver]
            ].min()

            self.__quantitiesDict["Altitude"] = float(
                np.interp(
                    self.__quantitiesDict[driver],
                    [x1, x2],
                    [
                        self.__data.loc[x1, "Altitude[km]"],
                        self.__data.loc[x2, "Altitude[km]"],
                    ],
                )
            )

        if driver == "Pressure":
            self.__quantitiesDict["Density"] = self.__quantitiesDict["Pressure"] / (
                287.052874 * self.__quantitiesDict["Temperature"]
            )

        elif driver == "Density":
            self.__quantitiesDict["Pressure"] = self.__quantitiesDict["Density"] * (
                287.052874 * self.__quantitiesDict["Temperature"]
            )
        self.__quantitiesDict["Speed of Sound"] = np.sqrt(
            1.4 * 287.052874 * self.__quantitiesDict["Temperature"]
        )
        self.__quantitiesDict["Viscosity"] = (
            1.458e-6
            * self.__quantitiesDict["Temperature"] ** 1.5
            / (self.__quantitiesDict["Temperature"] + 110.4)
        )

    def __model_only_lookup(self, driver: str) -> None:

        dataKey = self.__namedQuantitiesToDataMap[driver]
        self.__data.index = self.__data[dataKey]

        for key in self.__quantitiesDict.keys():
            if key in self.__excludeList:
                continue
            if key != driver:
                try:
                    self.__quantitiesDict[key] = self.__data.loc[
                        self.__quantitiesDict[driver],
                        self.__namedQuantitiesToDataMap[key],
                    ]
                except KeyError:
                    x1 = self.__data[dataKey][
                        self.__data[dataKey] < self.__quantitiesDict[driver]
                    ].max()
                    x2 = self.__data[dataKey][
                        self.__data[dataKey] > self.__quantitiesDict[driver]
                    ].min()
                    self.__quantitiesDict[key] = float(
                        np.interp(
                            self.__quantitiesDict[driver],
                            [x1, x2],
                            [
                                self.__data.loc[
                                    x1, self.__namedQuantitiesToDataMap[key]
                                ],
                                self.__data.loc[
                                    x2, self.__namedQuantitiesToDataMap[key]
                                ],
                            ],
                        )
                    )


if __name__ == "__main__":
    atm = Atmosphere()
    atm.help()
