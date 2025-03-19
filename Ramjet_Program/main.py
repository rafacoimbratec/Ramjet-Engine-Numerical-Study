import gui  # This will launch the GUI
import ramjet  # Import the ramjet function
import numpy as np

# Commenting out GUI launch
# if __name__ == "__main__":
#     gui.root.mainloop()  # Start the GUI

# Run ramjet calculations with example inputs
result = ramjet.calculations(0.1, 250, 3, 1.5, 0.5, 1750, 10000)
print("Calculation Results:")
print(f"Inlet Area (m²): {result[0]}")
print(f"Inlet Throat Area (m²): {result[1]}")
print(f"Burner Area (m²): {result[2]}")
print(f"Nozzle Throat Area (m²): {result[3]}")
print(f"Exhaust Area (m²): {result[4]}")
print(f"Thermal Efficiency (%): {result[5] * 100}")
print(f"Propulsive Efficiency (%): {result[6] * 100}")
