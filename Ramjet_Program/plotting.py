import matplotlib.pyplot as plt
import numpy as np
import ramjet  # Ensure the module is correctly referenced

def plot_ramjet_performance(P1, T1, M1, Ms, M2, Tb, Thrust):
    """
    Plots the design areas and performance parameters of a ramjet engine.
    
    Parameters:
    P1 : float - Free-stream pressure (Bar)
    T1 : float - Free-stream temperature (K)
    M1 : float - Flight Mach number
    Ms : float - Normal shock strength
    M2 : float - Burner entry Mach number
    Tb : float - Burner temperature (K)
    Thrust : float - Required thrust (N)
    """
    # Compute results
    A1, AC1, A2, AC2, A4, eta_thermal_cycle_real, eta_propulsive = ramjet.calculations(P1, T1, M1, Ms, M2, Tb, Thrust)

    # Ramjet schematic shape (simplified side view)
    x = [0, 1, 2, 3, 4, 5]
    y = [0, A1, AC1, A2, AC2, A4]
    y_symmetric = [-val for val in y]

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Plot schematic view of ramjet geometry
    axes[0].plot(x, y, label="Top contour", color="blue")
    axes[0].plot(x, y_symmetric, label="Bottom contour", color="blue")
    axes[0].fill_between(x, y, y_symmetric, color="lightblue", alpha=0.5)
    
    for i, label in enumerate(['Inlet (A1)', 'Throat (AC1)', 'Burner (A2)', 'Nozzle Throat (AC2)', 'Exhaust (A4)']):
        axes[0].annotate(label, (x[i+1], y[i+1]), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9, rotation=45)

    axes[0].set_title("Ramjet Engine Cross-Section (Schematic)")
    axes[0].axis('off')
    axes[0].set_aspect('equal')

    # Simulated Pressure, Temperature, and Mach trends along the nozzle
    x_positions = np.linspace(0, 1, 5)  # Normalized positions along nozzle
    pressures = np.array([P1, P1*0.9, P1*0.8, P1*0.6, P1*0.5])
    temperatures = np.array([T1, T1*1.1, T1*1.2, Tb*0.9, Tb])
    mach_numbers = np.array([M1, M1*0.8, M2, M2*1.2, M2*1.5])

    # Plot performance parameters
    axes[1].plot(x_positions, pressures, label="Pressure (Bar)", marker='o')
    axes[1].plot(x_positions, temperatures, label="Temperature (K)", marker='s')
    axes[1].plot(x_positions, mach_numbers, label="Mach Number", marker='^')
    axes[1].set_xlabel("Normalized Nozzle Position")
    axes[1].set_title("Ramjet Performance Along Nozzle")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()