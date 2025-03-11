import numpy as np
import matplotlib.pyplot as plt
from flight_conditions import get_flight_conditions
from inlet import compute_inlet_conditions

def plot_flight_conditions(params):
    """
    Generates plots for flight conditions: T1 (stagnation temperature) and P1 (stagnation pressure)
    varying with Mach number.
    
    Args:
        params (EngineParameters): Engine parameters for consistency.
    """

    # Define Mach numbers for simulation
    mach_numbers = np.array([0.4, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])

    # Define altitudes corresponding to each Mach number (from empirical data)
    altitudes = np.array([0, 3.6, 8.45, 12, 15, 16.6, 18.5, 20, 23.5, 26]) * 1000  # Convert km to meters

    # Initialize lists for results
    T1_values = []
    P1_values = []
    sigma_values = []

    # Compute inlet conditions for each Mach-altitude pair
    for M, H in zip(mach_numbers, altitudes):
        flight_conditions = get_flight_conditions(M, H, params)
        inlet_conditions = compute_inlet_conditions(flight_conditions, params)

        T1_values.append(inlet_conditions["stagnation_temperature"])
        P1_values.append(inlet_conditions["stagnation_pressure"] / 1000)  # Convert Pa to kPa
        sigma_values.append(inlet_conditions["pressure_recovery"])

    # === Plot: Altitude and T1 vs Mach Number ===
    fig, ax1 = plt.subplots(figsize=(8,5))

    ax1.plot(mach_numbers, altitudes / 1000, 'k^-', label="Flight trajectory altitude")  # Convert m to km
    ax1.set_xlabel("Flight Mach number")
    ax1.set_ylabel("Flight trajectory altitude H (km)", color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_ylim(0, 30)  # Set range from 0 to 30 km
    ax1.set_yticks(np.arange(0, 31, 5))  # Set ticks every 5 km
    
    # Create second y-axis for T1
    ax2 = ax1.twinx()
    ax2.plot(mach_numbers, T1_values, 'bo-', label="Intake recovered temperature")
    ax2.set_ylabel("Intake recovered temperature T1 (K)", color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylim(0, 1500)  # Set range from 0 to 1500 K
    ax2.set_yticks(np.arange(0, 1501, 300))  # Set ticks every 300 K
    plt.title("Variation of H and T1 with the Flight Mach Number")
    plt.show()

    # === Plot: σ and P1 vs Mach Number ===
    fig, ax1 = plt.subplots(figsize=(8,5))

    # Plot Pressure Recovery Coefficient
    ax1.plot(mach_numbers, sigma_values, 'k^-', label="Total pressure recovery coefficient")
    ax1.set_xlabel("Flight Mach number")
    ax1.set_ylabel("Total pressure recovery coefficient σ", color='black')
    ax1.tick_params(axis='y', labelcolor='black')
    ax1.set_ylim(0, 1)  # Set range from 0 to 1
    ax1.set_yticks(np.arange(0, 1.2, 0.2))  # Set ticks every 0.2

    # Create second y-axis for P1
    ax2 = ax1.twinx()
    ax2.plot(mach_numbers, P1_values, 'bo-', label="Intake recovered pressure")
    ax2.set_ylabel("Intake recovered pressure P1 (kPa)", color='blue')
    ax2.tick_params(axis='y', labelcolor='blue')
    ax2.set_ylim(0, 300)  # Set range from 0 to 300 kPa
    ax2.set_yticks(np.arange(0, 301, 50))  # Set ticks every 50 kPa
    
    plt.title("Variation of σ and P1 with the Flight Mach Number")
    plt.show()
