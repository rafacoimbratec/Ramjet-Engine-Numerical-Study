import numpy as np
import matplotlib.pyplot as plt
from ramjet import calculations  # Make sure calculations() is imported correctly


def run_design_case():
    print("Enter conditions for your ramjet design:")

    try:
        P1 = float(input("Free-stream Pressure P1 (Pa): "))
        T1 = float(input("Free-stream Temperature T1 (K): "))
        M1 = float(input("Flight Mach Number M1: "))
        Ms = float(input("Shock Strength Ms (>1): "))
        M2 = float(input("Burner Entry Mach Number M2 (0 < M2 < 1): "))
        Tb = float(input("Burner Temperature Tb (K): "))
        Thrust = float(input("Thrust Requirement (N): "))
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        return

    result = calculations(P1, T1, M1, Ms, M2, Tb, Thrust)
    A1, AC1, A2, AC2, A4 = result[0:5]
    eta_thermal, eta_propulsive, total_eta,real_eta_thermal = result[8:]
    temp_vs_ds, pressures, temperatures = result[5:8]
    stations = ['Inlet', 'Burner Entry', 'Burner Exit', 'Nozzle Exit']

    print("\n--- Design Results ---")
    print(f"Inlet Area (m²): {A1:.4f}")
    print(f"Inlet Throat Area (m²): {AC1:.4f}")
    print(f"Burner Area (m²): {A2:.4f}")
    print(f"Nozzle Throat Area (m²): {AC2:.4f}")
    print(f"Exhaust Area (m²): {A4:.4f}")
    print(f"Thermal Efficiency: {eta_thermal * 100:.2f}%")
    print(f"Real Thermal Efficiency: {real_eta_thermal * 100:.2f}%")
    print(f"Propulsive Efficiency: {eta_propulsive * 100:.2f}%")
    print(f"Total Efficiency: {total_eta * 100:.2f}%")

    # --- Plotting ---
    T_vals, ds_vals = zip(*temp_vs_ds)

    plt.figure()
    plt.scatter(ds_vals, T_vals, color='black')
    plt.xlabel("Δs (J/kg·K)")
    plt.ylabel("Temperature (K)")
    plt.title("Temperature vs Entropy Change")
    plt.grid(True)

    plt.figure()
    plt.scatter(stations, pressures, color='blue')
    plt.ylabel("Pressure (kPa)")
    plt.title("Pressure Variation Along Engine")
    plt.grid(True)

    plt.figure()
    plt.scatter(stations, temperatures, color='red')
    plt.ylabel("Temperature (K)")
    plt.title("Temperature Variation Along Engine")
    plt.grid(True)

    plt.show()


def run_parametric_study():
    print("Choose a parameter to vary:")
    print("1. Flight Mach Number (M1)")
    print("2. Free-stream Pressure (P1)")
    print("3. Free-stream Temperature (T1)")
    print("4. Shock Strength (Ms)")
    print("5. Burner Entry Mach (M2)")
    print("6. Burner Temperature (Tb)")
    print("7. Thrust")

    choice = input("Enter your choice [1-7]: ")

    x_vals = []
    eta_th, eta_prop, eta_total, real_eta_th = [], [], [], []
    T2_vals, T4_vals = [], []

    # Define parameter ranges and call calculations
    if choice == '1':
        x_vals = np.linspace(1, 5.55, 450)
        label = 'Flight Mach Number M1'
        for M1 in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(70e3, 210, M1, 1.1, 0.3, 1700, 50000)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)

    elif choice == '2':
        x_vals = np.linspace(1e3, 1e5, 200)
        label = 'Free-stream Pressure P1 (Pa)'
        for P1 in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(P1, 210, 2.8, 1.1, 0.2, 1700, 50000)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)

    elif choice == '3':
        x_vals = np.arange(200, 500)
        label = 'Free-stream Temperature T1 (K)'
        for T1 in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(70e3, T1, 2.8, 1.1, 0.2, 1700, 50000)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)

    elif choice == '4':
        x_vals = np.linspace(1.01, 1.8, 200)
        label = 'Shock Strength Ms'
        for Ms in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(70e3, 210, 2.8, Ms, 0.2, 1700, 50000)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)

    elif choice == '5':
        x_vals = np.linspace(0.01, 1, 200)
        label = 'Burner Entry Mach Number M2'
        for M2 in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(70e3, 210, 2.8, 1.1, M2, 1700, 50000)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)

    elif choice == '6':
        x_vals = np.arange(1500, 2001)
        label = 'Burner Temperature Tb (K)'
        for Tb in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(70e3, 210, 2.8, 1.1, 0.2, Tb, 50000)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)

    elif choice == '7':
        x_vals = np.linspace(1e3, 100e3, 200)
        label = 'Thrust (N)'
        for Thrust in x_vals:
            *_, eth, ep, etot, real, T2, T4 = calculations(70e3, 210, 2.8, 1.1, 0.2, 1700, Thrust)
            eta_th.append(eth)
            eta_prop.append(ep)
            eta_total.append(etot)
            real_eta_th.append(real)
            T2_vals.append(T2)
            T4_vals.append(T4)
    else:
        print("Invalid choice.")
        return

    # --- Plotting efficiencies ---
    plt.figure()
    plt.plot(x_vals, eta_prop, 'b', label='Propulsive Efficiency')
    plt.plot(x_vals, eta_th, 'r', label='Ideal Thermal Efficiency')
    plt.plot(x_vals, real_eta_th, 'y', label='Real Thermal Efficiency')
    plt.plot(x_vals, eta_total, 'g', label='Total Efficiency')
    plt.xlabel(label)
    plt.ylabel('Efficiency')
    plt.title(f'Efficiency vs {label}')
    plt.legend()
    plt.grid(True)

    # --- Plotting T2 and T4 ---
    plt.figure()
    plt.plot(x_vals, T2_vals, 'c', label='T2 (Burner Entry Temp)')
    plt.plot(x_vals, T4_vals, 'm', label='T4 (Nozzle Exit Temp)')
    plt.xlabel(label)
    plt.ylabel('Temperature (K)')
    plt.title(f'Temperatures T2 and T4 vs {label}')
    plt.legend()
    plt.grid(True)

    plt.show()



def main():
    print("====== RAMJET MODEL MENU ======")
    print("1. Evaluate a specific design case")
    print("2. Run a parametric study")
    choice = input("Enter your choice [1 or 2]: ")

    if choice == '1':
        run_design_case()
    elif choice == '2':
        run_parametric_study()
    else:
        print("Invalid selection. Please choose 1 or 2.")


if __name__ == '__main__':
    main()
