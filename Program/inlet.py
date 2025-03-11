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
    # --- Compute stag Temperature after intake compression ---
    T1 = T0 * (1 + ((gamma - 1) / 2) * M**2)

    # --- Compute Pressure Recovery Coefficient (σ) ---
    if M < 2:
        nk = 0.99
        sigma = nk
    elif 0.9 <= M <= 5:
        nk=0.9
        sigma = (1 + (((gamma - 1)*(1 - nk)) / 2) * M**2) ** ((-gamma) / (gamma - 1))
    else:
        sigma = 0.37  # Above Mach 5, severe losses
    # --- Compute Stagnation Pressure ---
    P1 = P0 * sigma


    return {
        "mach": M,
        "stagnation_temperature": T1,
        "stagnation_pressure": P1,
        "pressure_recovery": sigma,
    }
