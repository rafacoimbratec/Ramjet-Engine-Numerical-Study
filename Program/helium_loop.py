import numpy as np
from parameters import EngineParameters

def compute_helium_loop(air_compressor_conditions, params):
    """
    Computes the helium loop conditions after absorbing heat from the compressed air.

    Args:
        air_compressor_conditions (dict): Stagnation properties after the air compressor.
        params (EngineParameters): Engine parameters.

    Returns:
        dict: Helium loop conditions after heat exchange.
    """
    
    # Extract air compressor exit conditions
    T_air = air_compressor_conditions["stagnation_temperature"]  # Temperature after compressor (K)
    
    # Extract engine parameters
    cp_helium = params.CP_HELIUM  # Specific heat capacity of helium (J/kg·K)
    mass_flow_helium = params.HELIUM_FLOW_RATE  # Helium mass flow rate (kg/s)
    helium_temp_inlet = params.HELIUM_TEMP_INLET_HX2  # Initial helium temperature before heat exchange (K)
    helium_pressure = params.HELIUM_PRESSURE  # Helium operating pressure (Pa)
    
    # Assume helium absorbs a fraction of the heat from the air
    heat_transfer_efficiency = params.HELIUM_HEAT_TRANSFER_EFFICIENCY  # Efficiency factor
    heat_absorbed = heat_transfer_efficiency * mass_flow_helium * cp_helium * (T_air - helium_temp_inlet)
    
    # Compute new helium temperature after absorbing heat
    T_helium_out = helium_temp_inlet + (heat_absorbed / (mass_flow_helium * cp_helium))
    
    return {
        "helium_temperature": T_helium_out,
        "helium_pressure": helium_pressure,
        "heat_absorbed": heat_absorbed,
    }


def compute_helium_hx(helium_conditions, params):
    """
    Computes helium temperature and energy transfer through heat exchangers HX3 and HX4.

    Args:
        helium_conditions (dict): Helium conditions after the previous stage.
        params (EngineParameters): Engine parameters.

    Returns:
        dict: Updated helium conditions after HX3 and HX4.
    """
    # Extract helium properties
    T_helium_in = helium_conditions["helium_temperature"]
    mass_flow_helium = params.HELIUM_FLOW_RATE
    cp_helium = params.CP_HELIUM
    
    # === HX3: Helium transfers heat to Hydrogen ===
    hx3_efficiency = params.HX3_EFFICIENCY  # Efficiency factor
    T_hydrogen_in = params.HYDROGEN_TEMP_INLET_HX3  # Hydrogen inlet temp
    
    Q_hx3 = hx3_efficiency * mass_flow_helium * cp_helium * (T_helium_in - T_hydrogen_in)
    T_helium_after_hx3 = T_helium_in - (Q_hx3 / (mass_flow_helium * cp_helium))
    
    # === HX4: Helium transfers heat to LH2 Pump ===
    hx4_efficiency = params.HX4_EFFICIENCY
    T_lh2_pump_in = params.LH2_PUMP_TEMP_INLET
    
    Q_hx4 = hx4_efficiency * mass_flow_helium * cp_helium * (T_helium_after_hx3 - T_lh2_pump_in)
    T_helium_after_hx4 = T_helium_after_hx3 - (Q_hx4 / (mass_flow_helium * cp_helium))
    
    return {
        "helium_temperature": T_helium_after_hx4,
        "heat_transferred_hx3": Q_hx3,
        "heat_transferred_hx4": Q_hx4,
    }
