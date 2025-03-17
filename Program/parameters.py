import numpy as np

class EngineParameters:
    """ Defines constants and design parameters for the SABRE engine. """

    # === PHYSICAL CONSTANTS ===
    R_AIR = 287.05  # Specific gas constant for air (J/kg·K)
    R_HELIUM = 2077  # Specific gas constant for helium (J/kg·K)
    R_HYDROGEN = 4124  # Specific gas constant for hydrogen (J/kg·K)
    
    GAMMA_AIR = 1.4  # Heat capacity ratio for air
    GAMMA_HELIUM = 1.66  # Heat capacity ratio for helium
    GAMMA_HYDROGEN = 1.41  # Heat capacity ratio for hydrogen

    CP_AIR = 1005  # Specific heat at constant pressure for air (J/kg·K)
    CP_HELIUM = 5193  # Specific heat for helium (J/kg·K)
    CP_HYDROGEN = 14310  # Specific heat for hydrogen (J/kg·K)

    # === DESIGN PARAMETERS ===
    MACH_RANGE = np.linspace(0.4, 5.0, 10)  # Mach numbers for simulation
    ALTITUDE_RANGE = np.linspace(0, 30000, 10)  # Altitudes in meters
    
    INTAKE_EFFICIENCY = 0.95  # Intake pressure recovery factor
    COMPRESSOR_PRESSURE_RATIO = 20  # Turbo-compressor pressure ratio
    COMPRESSOR_EFFICIENCY = 0.85  # Isentropic efficiency of air compressor
    TURBINE_EFFICIENCY = 0.9  # Isentropic efficiency of turbines
    NOZZLE_EFFICIENCY = 0.98  # Nozzle expansion efficiency

    # === FUEL PARAMETERS ===
    LH2_TEMPERATURE = 20.27  # Liquid hydrogen temperature in Kelvin
    LH2_DENSITY = 70.85  # kg/m^3 (density of liquid hydrogen)
    HYDROGEN_LOWER_HEATING_VALUE = 120e6  # J/kg (energy content of hydrogen)
    
    # === HELIUM CYCLE PARAMETERS ===
    HELIUM_FLOW_RATE = 180  # kg/s (total helium mass flow)
    HELIUM_TEMP_INLET_HX1 = 600  # K (before entering precooler)
    HELIUM_TEMP_OUTLET_HX1 = 340  # K (after precooler)
    
    # === COMBUSTION CHAMBER PARAMETERS ===
    COMBUSTION_EFFICIENCY = 0.98
    CHAMBER_PRESSURE = 2.0e6  # 2 MPa (typical for airbreathing mode)
    MASS_FLOW_AIR = 382
    
    # === NOZZLE PARAMETERS ===
    NOZZLE_EXPANSION_RATIO = 50  # Area expansion ratio
    NOZZLE_EXIT_PRESSURE = 101325  # Exit pressure in Pascals (sea level)

    def __init__(self):
        """ Optionally, load additional configurations from a file. """
        pass

    def display(self):
        """ Prints all parameters for debugging. """
        for attr, value in self.__class__.__dict__.items():
            if not attr.startswith("__") and not callable(value):
                print(f"{attr}: {value}")

