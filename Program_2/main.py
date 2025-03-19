import numpy as np
from scipy.optimize import fsolve


k = 1.4  # Specific heat ratio for air
PR1, PR2, PR3, PR4 = 1.2, 1.3, 1.1, 1.5  # Pressure ratios (approximate)
Pfuel = 1e6  # Fuel pressure (assumed)
Tfuel = 300  # Fuel temperature (assumed)
Tf = 3200  # Combustion flame temperature (assumed)
PHe = 500000  # Helium cycle pressure (assumed)


def sabre_equations(vars):
    """ System of 43 equations for SABRE engine """

    # Given constants from the table (assumed values, adjust as needed)
    T4cal = 0
    T16cal = 0
    T22cal = 0
    T10cal = 0
    T13cal = 0
    T18cal = 0
    P4cal = 0
    P16cal = 0
    P22cal = 0
    P10cal = 0
    P13cal = 0
    P18cal = 0
    PR1, PR2, PR3, PR4 = 1.2, 1.3, 1.1, 1.5  # Example pressure ratios
    Pfuel = 0
    Tfuel=0
    Tf = 0
    PHe=0
    k = 1.4  # Specific heat ratio (adjust as needed)
    
    # Unpack variables (temperatures, pressures, mass flow rates, power)
    T = vars[:24]  # First 24 variables are temperatures
    P = vars[24:48]  # Next set of variables are pressures
    W = vars[48:50]  # Power equations
    m_air, m_fuel, m_ox, m_nozzle = vars[50:]  # Mass flow rates

    # Define the 43 equations
    eq1 = T[4] - T4cal
    eq2 = T[16] - T16cal
    eq3 = P[3] - P[4] - P4cal
    eq4 = P[23] - P[16] - P16cal
    eq5 = P[4] - P[5]
    eq6 = T[5] - T[4]
    eq7 = P[6] - P[5] * PR1
    eq8 = T[6] - T[5] * PR1**((k-1)/k)
    eq9 = P[6] - P[7]
    eq10 = T[7] - T[6]
    
    eq11 = Pfuel - P[9]
    eq12 = Tfuel - T[9]
    eq13 = T[22] - T22cal
    eq14 = T[10] - T10cal
    eq15 = P[21] - P[22] - P22cal
    eq16 = P[9] - P[10] - P10cal
    eq17 = P[10] / PR4 - P[11]
    eq18 = T[11] - T[10] / PR4**((k-1)/k)
    
    eq19 = (P[11] * m_fuel + P[7] * m_air / 1.2) / (m_air + m_fuel) - P[12]
    eq20 = T[12] - Tf
    eq21 = T[18] - T18cal
    eq22 = T[13] - T13cal
    eq23 = P[17] - P[18] - P18cal
    eq24 = P[12] - P[13] - P13cal
    eq25 = P[13] - P[14]
    eq26 = T[14] - T[13]
    
    eq27 = P[16] - P[17]
    eq28 = P[17] - P[16]
    eq29 = P[18] - T[19]
    eq30 = T[19] - T[18]
    
    eq31 = P[20] - P[19] / PR2
    eq32 = T[19] - T[20] * PR2**((k-1)/k)
    eq33 = P[20] - P[21]
    eq34 = T[21] - T[20]
    eq35 = P[22]*PR3 - P[23]
    eq36 = T[23] - T[22] * PR3**((k-1)/k)
    eq37 = P[3] - P[2]
    eq38 = T[3] - T[2]
    
    eq39 = P[23] - PHe
    eq40 = W[0] - W[1] #W5-6 - W19-20
    eq41 = W[2] - W[3] #W10-11 - W22-23
    eq42 = P[7] - P[13]
    
    eq43 = m_air + m_fuel + m_ox - m_nozzle  # Mass conservation
    
    # Extend the list to include all 43 equations
    equations = [
        eq1, eq2, eq3, eq4, eq5, eq6, eq7, eq8, eq9, eq10,
        eq11, eq12, eq13, eq14, eq15, eq16, eq17, eq18, eq19, eq20,
        eq21, eq22, eq23, eq24, eq25, eq26, eq27, eq28, eq29, eq30,
        eq31, eq32, eq33, eq34, eq35, eq36, eq37, eq38, eq39, eq40,
        eq41, eq42, eq43
    ]

    return equations

# Initial guesses for solving (temperature, pressure, power, mass flows)
initial_guesses = np.ones(54) * 300  # Adjust based on real values

# Solve the system
solution = fsolve(sabre_equations, initial_guesses)

# Print solution
print("Solution:", solution)



def effectiveness_ntu(NTU, C_r):
    """ Effectiveness calculation for a cross-flow heat exchanger """
    return 1 - np.exp(1 / C_r * NTU ** 0.78 * (np.exp(-C_r * NTU ** 0.22) - 1))

# ================================
# Heat Exchanger Model
# ================================

def heat_exchanger(Q_dot_max, NTU, C_r):
    """ Compute heat transfer using NTU method """
    effectiveness = 1 - np.exp(1 / C_r * NTU ** 0.78 * (np.exp(-C_r * NTU ** 0.22) - 1))
    Q_dot = effectiveness * Q_dot_max  # Heat transfer
    return Q_dot

def precooler_simulation(layers=56, nodes=10):
    """ Simulate precooler as per paper's 2D model """
    T_air = np.linspace(1000, 123, layers)
    T_helium = np.linspace(80, 175, layers)

    for i in range(1, layers):
        for j in range(1, nodes):
            dT_air = (T_air[i-1] - T_air[i]) * 0.1
            dT_helium = (T_helium[i-1] - T_helium[i]) * 0.1
            T_air[i] -= dT_air
            T_helium[i] += dT_helium

    return T_air, T_helium

T_air_out, T_helium_out = precooler_simulation()
print("Air Outlet Temperatures:", T_air_out)
print("Helium Outlet Temperatures:", T_helium_out)

# ================================
# Run Full SABRE Simulation
# ================================

def sabre_simulation(Mach, altitude):
    """ Full SABRE engine simulation """
    solution = fsolve(sabre_equations, initial_guesses)
    Q_dot_max = 50  
    NTU = 5  
    C_r = 0.8  
    heat_transfer = heat_exchanger(Q_dot_max, NTU, C_r)
    thrust = 100 + 0.5 * Mach * heat_transfer  
    return thrust, solution




thrust, engine_params = sabre_simulation(Mach=4, altitude=25000)
print("Thrust:", thrust, "kN")
print("Engine Parameters:", engine_params)