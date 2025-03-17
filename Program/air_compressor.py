import numpy as np
from parameters import EngineParameters

def compute_air_compressor(precooler_conditions, params):
    """
    Computes the air compression process in the SABRE engine.

    Args:
        precooler_conditions (dict): Stagnation properties after the precooler.
        params (EngineParameters): Engine parameters.

    Returns:
        dict: Stagnation properties after the air compressor.
    """
    
    # Extract incoming air conditions
    T1 = precooler_conditions["stagnation_temperature"]  # Stagnation temperature after precooler (K)
    P1 = precooler_conditions["stagnation_pressure"]  # Stagnation pressure after precooler (Pa)
    
    # Extract engine parameters
    cp_air = params.CP_AIR  # Specific heat capacity of air (J/kg·K)
    gamma_air = params.GAMMA_AIR  # Heat capacity ratio of air
    compressor_pressure_ratio = params.COMPRESSOR_PRESSURE_RATIO  # Compression ratio
    compressor_efficiency = params.COMPRESSOR_EFFICIENCY  # Efficiency factor
    
    # Compute pressure after compression
    P2 = P1 * compressor_pressure_ratio
    
    # Compute temperature after compression using isentropic relation with efficiency factor
    T2_isentropic = T1 * (compressor_pressure_ratio ** ((gamma_air - 1) / gamma_air))
    T2 = T1 + (T2_isentropic - T1) / compressor_efficiency
    
    return {
        "stagnation_temperature": T2,
        "stagnation_pressure": P2,
    }
