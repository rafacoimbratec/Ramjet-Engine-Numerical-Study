import numpy as np
from parameters import EngineParameters

def compute_inlet_conditions(flight_conditions, params):
    """
    Computes intake conditions (stagnation temperature & pressure).

    Args:
        flight_conditions (dict): Atmospheric properties at flight conditions.
        params (EngineParameters): Engine constants.

    Returns:
        dict: Stagnation temperature and pressure at intake.
    """

    # Extract ambient conditions
    M = flight_conditions["mach"]  # Mach number
    T0 = flight_conditions["temperature"]  # Static temperature (K)
    P0 = flight_conditions["pressure"]  # Static pressure (Pa)

    gamma = params.GAMMA_AIR  # Heat capacity ratio for air

    # --- Compute Stagnation Temperature after intake compression ---
    T1 = T0 * (1 + ((gamma - 1) / 2) * M**2)

    # --- Compute Pressure Recovery Coefficient (σ) --- #WE NEED TO MAKE THIS BETTER IF THE CONCLUSIONS ARE NOT GOOD
    if M < 1:
        sigma = 1 - 0.02 * M**2  # Very mild loss in subsonic flow
    elif 1 <= M < 2:
        sigma = 0.98 - 0.1 * (M - 1)  # Linear drop in transonic region
    elif 2 <= M < 3:
        sigma = 0.88 - 0.3 * (M - 2)  # Steeper drop due to normal shock losses
    else:
        sigma = 0.63 * np.exp(-0.7 * (M - 3))  # Exponential decay in hypersonic flow
        

    # --- Compute Stagnation Pressure ---
    P1 = P0 * sigma  #rad !!! https://www.grc.nasa.gov/www/k-12/airplane/tunmodinlt.html
    P1 = P1 * (1 + ((gamma - 1) / 2) * M**2)**((gamma) / (gamma - 1))
    print(P1*10**-5)
    return {
        "mach": M,
        "stagnation_temperature": T1,
        "stagnation_pressure": P1,
        "pressure_recovery": sigma,
    }

