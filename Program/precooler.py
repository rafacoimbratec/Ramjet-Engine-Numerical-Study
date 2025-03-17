import numpy as np
from parameters import EngineParameters

def compute_precooler(inlet_conditions, params):
    """
    Computes air cooling in the precooler using helium heat exchange.

    Args:
        inlet_conditions (dict): Stagnation properties after intake.
        params (EngineParameters): Engine parameters.

    Returns:
        dict: Stagnation properties after the precooler.
    """

    # Extract incoming air conditions
    T1 = inlet_conditions["stagnation_temperature"]  # Stagnation temp after intake (K)
    P1 = inlet_conditions["stagnation_pressure"]  # Stagnation pressure after intake (Pa)

    # Extract engine parameters
    cp_air = params.CP_AIR  # Specific heat capacity of air (J/kg·K)
    cp_helium = params.CP_HELIUM  # Specific heat capacity of helium (J/kg·K)
    mass_flow_air = params.MASS_FLOW_AIR  # Mass flow rate of air (kg/s)
    mass_flow_helium = params.HELIUM_FLOW_RATE  # Helium mass flow (kg/s)
    precooler_efficiency = 0.95  # 95% efficiency factor

    # Define precooler exit temperature (assumed target temperature for now)
    T2_target = 150  # K (Example: Cooled air target temp)

    # Compute required heat exchange (Q = m * Cp * ΔT)
    Q_air = mass_flow_air * cp_air * (T1 - T2_target)
    Q_helium = mass_flow_helium * cp_helium * (params.HELIUM_TEMP_INLET_HX1 - params.HELIUM_TEMP_OUTLET_HX1)
    
    # Apply precooler efficiency
    Q_actual = Q_air * precooler_efficiency

    # Verify feasibility of cooling process
    if Q_actual > Q_helium:
        raise ValueError("Helium cooling capacity is insufficient!")

    # Compute actual exit temperature of air
    T2 = T1 - (Q_actual / (mass_flow_air * cp_air))

    # Apply small stagnation pressure loss (due to cooling)
    pressure_drop_factor = 0.98  # Example: 2% pressure loss
    P2 = P1 * pressure_drop_factor

    return {
        "stagnation_temperature": T2,
        "stagnation_pressure": P2,
        "heat_removed": Q_actual,
    }
