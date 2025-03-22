import numpy as np
import matplotlib.pyplot as plt
from ramjet import calculations  # Your updated calculations function
'''
# Run ramjet calculations with example inputs
result = calculations(70e3, 210, 3.25, 1.2, 0.3, 1800, 10e3)

A1, AC1, A2, AC2, A4 = result[0:5]
eta_thermal, eta_propulsive, total_eta = result[8:]
temp_vs_ds, pressures, temperatures = result[5:8]

# Print basic outputs
print(f"Inlet Area (m²): {A1:.4f}")
print(f"Inlet Throat Area (m²): {AC1:.4f}")
print(f"Burner Area (m²): {A2:.4f}")
print(f"Nozzle Throat Area (m²): {AC2:.4f}")
print(f"Exhaust Area (m²): {A4:.4f}")
print(f"Thermal Efficiency: {eta_thermal * 100:.2f}%")
print(f"Propulsive Efficiency: {eta_propulsive * 100:.2f}%")
print(f"Total Efficiency: {total_eta * 100:.2f}%")

# ---- PLOT SECTION ----
stations = ['Inlet', 'Burner Entry', 'Burner Exit', 'Nozzle Exit']

# 1. Temperature vs Δs
T_vals, ds_vals = zip(*temp_vs_ds)
plt.figure()
plt.scatter(ds_vals, T_vals, color='black')
plt.xlabel("Δs (J/kg·K)")
plt.ylabel("Temperature (K)")
plt.title("Temperature vs Entropy Change")
plt.grid(True)

# 2. Pressure variation
plt.figure()
plt.scatter(stations, pressures, color='blue')
plt.ylabel("Pressure (Bar)")
plt.title("Pressure Variation Along Engine")
plt.grid(True)

# 3. Temperature variation
plt.figure()
plt.scatter(stations, temperatures, color='red')
plt.ylabel("Temperature (K)")
plt.title("Temperature Variation Along Engine")
plt.grid(True)

plt.show()

'''
def parametric_study():
    # 1. Vary Flight Mach Number M1
    M1_vals = np.linspace(1, 5.5, 450)
    eta_th, eta_prop, eta_total = [], [], []
    for M1 in M1_vals:
        *_, eth, ep,total = calculations(70e3, 210, M1, 1.1, 0.2, 1700, 50000)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(M1_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(M1_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(M1_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Flight Mach Number M1')
    plt.ylabel('Efficiency')
    plt.title('Effect of Flight Mach Number')
    plt.legend()
    plt.grid(True)

    # 2. Vary Free-Stream Pressure P1
    P1_vals = np.linspace(0, 1e5, 200)
    eta_th, eta_prop, eta_total = [], [], []
    for P1 in P1_vals:
        *_, eth, ep,total = calculations(P1, 210, 2.8, 1.1, 0.2, 1700, 50000)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(P1_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(P1_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(P1_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Free-stream Pressure P1 (Pa)')
    plt.ylabel('Efficiency')
    plt.title('Effect of Free-stream Pressure')
    plt.legend()
    plt.grid(True)

    # 3. Vary Free-Stream Temperature T1
    T1_vals = np.arange(0, 500)
    eta_th, eta_prop, eta_total = [], [], []
    for T1 in T1_vals:
        *_, eth, ep,total = calculations(70e3, T1, 2.8, 1.1, 0.2, 1700, 50000)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(T1_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(T1_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(T1_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Free-stream Temperature T1 (K)')
    plt.ylabel('Efficiency')
    plt.title('Effect of Free-stream Temperature')
    plt.legend()
    plt.grid(True)

    # 4. Vary Normal Shock Strength Ms
    Ms_vals = np.linspace(1.01, 1.8, 200)
    eta_th, eta_prop, eta_total = [], [], []
    for Ms in Ms_vals:
        *_, eth, ep, total = calculations(70e3, 210, 2.8, Ms, 0.2, 1700, 50000)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(Ms_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(Ms_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(Ms_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Normal Shock Strength Ms')
    plt.ylabel('Efficiency')
    plt.title('Effect of Shock Strength')
    plt.legend()
    plt.grid(True)

    # 5. Vary Burner Entry Mach Number M2
    M2_vals = np.linspace(0, 1, 200)
    eta_th, eta_prop, eta_total = [], [], []
    for M2 in M2_vals:
        *_, eth, ep,total = calculations(70e3, 210, 2.8, 1.1, M2, 1700, 50000)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(M2_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(M2_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(M2_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Burner Entry Mach Number M2')
    plt.ylabel('Efficiency')
    plt.title('Effect of Burner Entry Mach')
    plt.legend()
    plt.grid(True)

    # 6. Vary Burner Temperature Tb
    Tb_vals = np.arange(1500, 2001)
    eta_th, eta_prop, eta_total = [], [], []
    for Tb in Tb_vals:
        *_, eth, ep,total = calculations(70e3, 210, 2.8, 1.1, 0.2, Tb, 50000)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(Tb_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(Tb_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(Tb_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Burner Temperature Tb (K)')
    plt.ylabel('Efficiency')
    plt.title('Effect of Burner Temperature')
    plt.legend()
    plt.grid(True)

    # 7. Vary Thrust
    Thrust_vals = np.linspace(0, 100e3, 200)
    eta_th, eta_prop, eta_total = [], [], []
    for T in Thrust_vals:
        *_, eth, ep, total = calculations(70e3, 210, 2.8, 1.1, 0.2, 1700, T)
        eta_th.append(eth)
        eta_prop.append(ep)
        eta_total.append(total)

    plt.figure()
    plt.plot(Thrust_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(Thrust_vals, eta_th, 'r', label='Thermal Efficiency')
    plt.plot(Thrust_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel('Thrust (N)')
    plt.ylabel('Efficiency')
    plt.title('Effect of Thrust Requirement')
    plt.legend()
    plt.grid(True)

    plt.show()

if __name__ == '__main__':
   parametric_study()
