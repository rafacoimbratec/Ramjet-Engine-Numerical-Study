import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton

g = 9.81  # Gravity (m/s^2)
R = 287  # Specific gas constant for air (J/kg.K)
k = 1.4  # Adiabatic index for air
eta_c = 0.85  # Compressor efficiency
eta_t = 0.9  # Turbine efficiency
eta_comb = 0.98  # Combustion efficiency
eta_pump = 0.85  # Pump efficiency
eta_hx = 0.95  # Heat exchanger efficiency
q_H2 = 120e6  # Hydrogen lower heating value (J/kg)

# Flight conditions
H = 20e3  # Altitude (m)
P0 = 2.24e4  # Ambient pressure (Pa)
T0 = 216.5  # Ambient temperature (K)

# Define helium and hydrogen flow rates
m_He = 180  # kg/s
m_H2 = 12.9  # kg/s
m_air = 382  # kg/s

# Define combustion chamber parameters
Pcc = 2e6  # Combustion chamber pressure (Pa)
T9 = 850  # Helium inlet temperature (K)

# Precooler & Heat Exchanger parameters
Cp_air = 1005  # Specific heat capacity of air (J/kg.K)
Cp_He = 5193  # Specific heat capacity of helium (J/kg.K)
T_He_in = 300  # Initial helium temperature (K)
precooler_eff = 0.9  # Precooler effectiveness

def intake_conditions(M, P0, T0):
    P3 = P0 * (1 + (k-1)/2 * M**2) ** (k/(k-1))
    T3 = T0 * (1 + (k-1)/2 * M**2)
    return P3, T3

def precooler(T3, T_He_in, m_air, m_He, Cp_air, Cp_He, precooler_eff):
    T_air_out = T3 - precooler_eff * (T3 - T_He_in)
    T_He_out = T_He_in + (m_air * Cp_air * (T3 - T_air_out)) / (m_He * Cp_He)
    return T_air_out, T_He_out

def turbo_compressor(P3, T3, Pcc, eta_c):
    P4 = Pcc
    T4 = T3 * (P4/P3) ** ((k-1)/(k * eta_c))
    return P4, T4

def helium_heat_exchanger(T_He_in, T4, eta_hx):
    T_He_out = T_He_in + eta_hx * (T4 - T_He_in)
    return T_He_out

def preburner(T_He_out, m_H2, m_He, q_H2, eta_comb):
    T5 = T_He_out + (m_H2 * q_H2 * eta_comb) / (m_He * Cp_He)
    return T5

def helium_turbine(T5, eta_t):
    T6 = T5 * (1 - eta_t)
    return T6

def nozzle_expansion(T6, Pcc, P0):
    T8 = T6 * (P0 / Pcc) ** ((k-1)/k)
    v8 = np.sqrt(2 * k * R * T8 / (k-1))
    return T8, v8

Mach_numbers = np.linspace(0, 5, 20)
Fs_values = []
Isp_values = []

for M in Mach_numbers:
    P3, T3 = intake_conditions(M, P0, T0)
    T3_cooled, T_He_out = precooler(T3, T_He_in, m_air, m_He, Cp_air, Cp_He, precooler_eff)
    P4, T4 = turbo_compressor(P3, T3_cooled, Pcc, eta_c)
    T_He_hx = helium_heat_exchanger(T_He_out, T4, eta_hx)
    T5 = preburner(T_He_hx, m_H2, m_He, q_H2, eta_comb)
    T6 = helium_turbine(T5, eta_t)
    T8, v8 = nozzle_expansion(T6, Pcc, P0)
    
    F = m_air * (v8 - M * np.sqrt(k * R * T0))
    Fs = F / m_air
    Isp = F / (m_H2 * g)
    
    Fs_values.append(Fs)
    Isp_values.append(Isp)

plt.figure(figsize=(10, 5))
plt.plot(Mach_numbers, Fs_values, label='Specific Thrust (Fs)')
plt.plot(Mach_numbers, Isp_values, label='Specific Impulse (Isp)')
plt.xlabel('Mach Number')
plt.ylabel('Performance Metrics')
plt.title('Specific Thrust and Specific Impulse vs Mach Number')
plt.legend()
plt.grid()
plt.show()
