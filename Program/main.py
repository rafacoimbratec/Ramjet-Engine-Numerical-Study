import numpy as np
from parameters import EngineParameters
from flight_conditions import get_flight_conditions
from inlet import compute_inlet_conditions
from output import plot_flight_conditions 
from precooler import compute_precooler
import matplotlib.pyplot as plt

def main():
    """ Main function to perform the preliminary design of a SABRE engine """
    
    # === Initialize Engine Parameters ===
    params = EngineParameters()
    
    # Display parameters (for debugging)
    print("\n--- Engine Parameters ---")
    params.display()

    # === Define Flight Conditions ===
    mach_number = 0.4  # Example: Mach 4
    altitude = 0  # 20 km in meters

    print(f"\nStarting SABRE Engine Simulation at Mach {mach_number}, Altitude {altitude} m...\n")

    # === Get Atmospheric Conditions ===
    flight_conditions = get_flight_conditions(mach_number, altitude, params)

    print("\n--- Flight Conditions 0 ---")
    units = {
        "altitude": "m",
        "mach": "",
        "temperature": "K",
        "pressure": "Pa",
        "density": "kg/m³",
        "speed_of_sound": "m/s",
        "velocity": "m/s",
    }

    for key, value in flight_conditions.items():
        print(f"{key}: {value:.3f} {units[key]}")

    # === Compute Inlet Conditions ===
    inlet_conditions = compute_inlet_conditions(flight_conditions, params)

    print("\n--- Inlet Conditions 1 ---")
    units_inlet = {
        "mach": "",
        "stagnation_temperature": "K",
        "stagnation_pressure": "Pa",
        "pressure_recovery": "",
    }

    for key, value in inlet_conditions.items():
        print(f"{key}: {value:.3f} {units_inlet[key]}")

    # === Call Plotting Function to verify the values of Intake ===
    plot_flight_conditions(params)
    # === ===
     
    # === Compute Precooler Conditions ===
    precooler_conditions = compute_precooler(inlet_conditions, params)

    print("\n--- Precooler Conditions ---")
    units_precooler = {
    "stagnation_temperature": "K",
    "stagnation_pressure": "Pa",
    "heat_removed": "J",
    }

    for key, value in precooler_conditions.items():
        print(f"{key}: {value:.3f} {units_precooler[key]}")
    #air_compressor_conditions = compute_air_compressor(precooler_conditions, params)
    #helium_conditions = compute_helium_loop(air_compressor_conditions, params)
    #hydrogen_conditions = compute_hydrogen_path(helium_conditions, params)
    #combustion_conditions = compute_combustion(hydrogen_conditions, params)
    #nozzle_conditions = compute_nozzle(combustion_conditions, params)

    # === Solve Full Thermodynamic Cycle ===
    #engine_performance = solve_cycle(nozzle_conditions, params)

    # === Display Results ===
    #display_results(engine_performance)

if __name__ == "__main__":
    main()
