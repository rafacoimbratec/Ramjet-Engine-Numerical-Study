import numpy as np
from parameters import EngineParameters

def get_flight_conditions(mach, altitude, params):
    """
    Computes atmospheric conditions (T, P, ρ) based on altitude.
    
    Args:
        mach (float): Flight Mach number.
        altitude (float): Altitude in meters.
        params (EngineParameters): Engine constants.
    
    Returns:
        dict: A dictionary containing atmospheric properties.
    """

    # --- Define ISA Layers (up to 32 km) ---
    layers = [
        {"h": 0, "T": 288.15, "L": -0.0065, "P": 101325},  # Sea level
        {"h": 11000, "T": 216.65, "L": 0.0, "P": 22632.1},  # Tropopause
        {"h": 20000, "T": 216.65, "L": 0.001, "P": 5474.89},  # Stratosphere
        {"h": 32000, "T": 228.65, "L": 0.0028, "P": 868.02},  # Upper stratosphere
    ]

    # --- Find the appropriate ISA layer ---
    for i in range(len(layers) - 1):
        if layers[i]["h"] <= altitude < layers[i + 1]["h"]:
            base = layers[i]
            break
    else:
        raise ValueError("Altitude out of range (must be below 32 km)")

    # --- Compute Temperature at Altitude ---
    T = base["T"] + base["L"] * (altitude - base["h"])

    # --- Compute Pressure Using Hydrostatic Equation ---
    if base["L"] == 0:
        # Isothermal Layer (T constant)
        P = base["P"] * np.exp(-9.80665 * (altitude - base["h"]) / (287.05 * base["T"]))
    else:
        # Non-Isothermal Layer
        P = base["P"] * (T / base["T"]) ** (-9.80665 / (base["L"] * 287.05))

    # --- Compute Density Using Ideal Gas Law ---
    rho = P / (params.R_AIR * T)

    # --- Compute Speed of Sound ---
    a = np.sqrt(params.GAMMA_AIR * params.R_AIR * T)

    # --- Compute Freestream Velocity ---
    V = mach * a

    # --- Return Conditions as Dictionary ---
    return {
        "altitude": altitude,
        "mach": mach,
        "temperature": T,
        "pressure": P,
        "density": rho,
        "speed_of_sound": a,
        "velocity": V,
    }
