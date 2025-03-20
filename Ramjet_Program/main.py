import gui  # This will launch the GUI
import ramjet  # Import the ramjet function
import numpy as np

# Commenting out GUI launch
# if __name__ == "__main__":
#     gui.root.mainloop()  # Start the GUI

AC1 = 0.0230 
A2  = 0.0683 
AC2 = 0.0390 
A4 = 0.1417 

# Run ramjet calculations with example inputs
result = ramjet.calculations(70e3,210,2.8,1.1,0.2,1700,50e3)
print("Calculation Results:")
print(f"Inlet Area (m²): {result[0]}")
print(f"Inlet Throat Area (m²): {result[1]}")
print(f"Burner Area (m²): {result[2]}")
print(f"Nozzle Throat Area (m²): {result[3]}")
print(f"Exhaust Area (m²): {result[4]}")
print(f"Thermal Efficiency (%): {result[5] * 100}")
print(f"Propulsive Efficiency (%): {result[6] * 100}")
