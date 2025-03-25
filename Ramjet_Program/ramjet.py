import numpy as np

def calculations(P1, T1, M1, Ms, M2, Tb, Thrust):
    """
    Computes key parameters for a ramjet engine.

    Parameters:
    P1 : float - Free-stream pressure (Bar)
    T1 : float - Free-stream temperature (K)
    M1 : float - Flight Mach number
    Ms : float - Normal shock strength
    M2 : float - Burner entry Mach number
    Tb : float - Burner temperature (K)
    Thrust : float - Required thrust (N)

    Returns:
    A1, AC1, A2, AC2, A4 : float - Various area parameters
    temp_vs_ds : list of (T, Δs) - Temperature vs Entropy change across stages
    pressures : list - Pressure at key stations (Bar)
    temperatures : list - Temperature at key stations (K)
    eta_thermal_cycle_real : float - Thermal efficiency
    eta_propulsive : float - Propulsive efficiency
    total_eta : float - Overall cycle efficiency
    """
    
    # --- CONSTANTS ---
    gamma = 1.4                      # Ratio of specific heats for air
    R = 287                          # Specific gas constant for air (J/kg.K)
    cp_air = gamma * R / (gamma - 1)  # Specific heat at constant pressure
    

    # --- Inlet properties ---
    a1 = np.sqrt(gamma * R * T1)     # Speed of sound at inlet (m/s)
    U1 = a1 * M1                     # Free-stream velocity (m/s)
    air_density = P1 * 10**5 / (R * T1)  # Air density at inlet (kg/m³)

    # --- Combustion fuel properties (H2) ---
    q = 119.96 * 10**6               # Lower heating value of H2 (J/kg)
    cp_h2 = 14.3 * 1000              # Specific heat of H2 (converted to J/kg.K)
    f_stoich = 2.91 / 100            # Stoichiometric fuel-air ratio

    # --- Isentropic compression in the diffuser (to point 02') ---
    A1_over_AC1star = (1/M1)*((1+((gamma-1)/2)*M1**2)/((gamma+1)/2))**((gamma+1)/(2*(gamma-1)))
    T1_over_T0x = 1/(1 + ((gamma-1)/2)*M1**2)
    P1_over_P0x = (1 + ((gamma-1)/2)*M1**2)**(-gamma/(gamma-1))

    # --- Normal shock (from Ms to subsonic) ---
    M_y = np.sqrt((Ms**2 + 2/(gamma - 1)) / (2*gamma/(gamma - 1)*Ms**2 - 1))
    Ty_over_Tx = ((2 * gamma * Ms**2 - (gamma - 1)) * (2 + (gamma - 1) * Ms**2)) / ((gamma + 1)**2 * Ms**2)
    Ty_over_T0y = 1 / (1 + (gamma - 1) * M_y**2)
    Py_over_Px = (1 + Ms**2) / (1 + M_y**2)
    Ax_over_Aystar = (1/M_y)*((1+((gamma-1)/2)*M_y**2)/((gamma+1)/2))**((gamma+1)/(2*(gamma-1)))
    Tx_over_T0x = 1 / (1 + ((gamma - 1)/2)*Ms**2)
    Ax_over_AC1star = (1/Ms)*((1+((gamma - 1)/2)*Ms**2)/((gamma + 1)/2))**((gamma + 1)/(2*(gamma - 1)))

    # --- Burner Entry (subsonic flow at point 2) ---
    A2_over_Aystar = (1/M2)*((1+((gamma-1)/2)*M2**2)/((gamma+1)/2))**((gamma+1)/(2*(gamma-1)))
    T2_over_T0y = 1 / (1 + (gamma - 1) * M2**2)
    P2_over_P02 = (1 + ((gamma - 1)/2)*M2**2)**(-gamma/(gamma - 1))
    A2_over_A1 = (A2_over_Aystar / Ax_over_Aystar) * (Ax_over_AC1star / A1_over_AC1star)
    T2_over_T1 = T2_over_T0y / Ty_over_T0y * Ty_over_Tx * Tx_over_T0x / T1_over_T0x
    T2 = T1 * T2_over_T1

    # --- Burner (combustion at constant pressure, from T2 to Tb) ---
    P0y_over_P0x = ((2*gamma*Ms**2 - (gamma - 1)) / (gamma + 1))**(-1/(gamma - 1)) * (((gamma + 1)*Ms**2)/(2 + (gamma - 1)*Ms**2))**(gamma/(gamma - 1))
    P2_over_P0y = (1 + ((gamma - 1)/2)*M2**2)**(-gamma/(gamma - 1))
    P2_over_P1 = P2_over_P0y * P0y_over_P0x / P1_over_P0x
    Pb = P1 * P2_over_P1

    # Exit of burner
    Mb = M2 * np.sqrt(Tb / T2)  # Assuming constant pressure combustion
    Ab_over_AC2 = (1/Mb)*((1+((gamma - 1)/2)*Mb**2)/((gamma + 1)/2))**((gamma + 1)/(2*(gamma - 1)))
    Tb_over_T0b = 1 / (1 + (gamma - 1) * Mb**2)
    AC2_over_A1 = A2_over_A1 / Ab_over_AC2

    # --- Nozzle (isentropic expansion to ambient) ---
    Pb_over_P0b = (1 + ((gamma - 1)/2)*Mb**2)**(-gamma/(gamma - 1))
    P4_over_Pob = (P2_over_P1**-1) * Pb_over_P0b  # Back pressure assumed = P1
    T4_over_Tob = P4_over_Pob**((gamma - 1)/gamma)
    T0b_over_Tb = 1 + ((gamma - 1)/2) * Mb**2
    T4_over_Tb = T4_over_Tob * T0b_over_Tb
    T4 = Tb * T4_over_Tb

    M4 = np.sqrt((1/T4_over_Tob - 1) * 2 / (gamma - 1))
    A4_over_AC2 = (1/M4)*((1+((gamma - 1)/2)*M4**2)/((gamma + 1)/2))**((gamma + 1)/(2*(gamma - 1)))
    U4 = M4 * np.sqrt(gamma * R * T4_over_Tb * Tb)
    A4_over_A1 = A4_over_AC2 * AC2_over_A1

    # --- Area Calculations ---
    A1 = Thrust / (P1 * gamma * M1**2 * ((M4**2 / M1**2) * A4_over_A1 - 1))  # Inlet area from thrust
    A2 = A2_over_A1 * A1
    AC1 = A1 / A1_over_AC1star
    AC2 = A1 * AC2_over_A1
    A4 = A4_over_A1 * A1

    # --- Fuel flow estimation ---
    mf = cp_h2 * (Tb - T2) / q        # Fuel mass flow rate (kg/s)
    rho_f = mf / A2                   # Approximate fuel density per unit area (not used further)
    m_air = (P1 * A1) / (R * T1) * M1 * np.sqrt(gamma / (R * T1))  # Air mass flow (kg/s)
    sum_m = m_air + mf               # Total mass flow (air + fuel), used for analysis if needed

    # --- Efficiency Calculations ---
    eta_thermal_cycle_real = 1-T1/T2 #(Tb - T2 - T4 + T1) / (Tb - T2)  # Net mech output / heat input #Ideal ramjet cycle efficiency
    eta_propulsive = 2 / (1 + U4 / U1)                        # Thrust power / mech output
    real_eta_thermal_cycle = (Tb-T2-T4+T1)/(Tb-T2)  # Real thermal efficiency
    total_eta = real_eta_thermal_cycle * eta_propulsive

    # --- Specific Thrust ---
    specific_thrust = Thrust / (air_density * A1 * U1)

    # --- Profiles: Pressure, Temperature, Entropy ---
    temperatures = [T1, T2, Tb, T4]  # At inlet, burner entry, burner exit, nozzle exit
    pressures = [P1 * 1e-5, P2_over_P1 * P1 * 1e-5, Pb * 1e-5, P1 * 1e-5]  # Converted to bar
    temp_vs_ds = []

    # Calculate entropy change (ds) at each stage relative to the inlet
    s1 = cp_air * np.log(T1) - R * np.log(P1 * 1e5)
    for T, P in zip(temperatures, pressures):
        s = cp_air * np.log(T) - R * np.log(P * 1e5)
        temp_vs_ds.append((T, s - s1))

    return A1, AC1, A2, AC2, A4, temp_vs_ds, pressures, temperatures, eta_thermal_cycle_real, eta_propulsive, total_eta, real_eta_thermal_cycle, T2, T4
