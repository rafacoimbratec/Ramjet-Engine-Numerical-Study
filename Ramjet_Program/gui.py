import tkinter as tk
from tkinter import messagebox
import ramjet
from plotting import plot_ramjet_performance  # Import the plotting function

def validate_input(value, lower, upper):
    try:
        val = float(value)
        if lower <= val <= upper:
            return val
        else:
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", f"Value must be between {lower} and {upper}")
        return None

def submit():
    values = {
        "P1": validate_input(p1_entry.get(), 0.025, 0.4854),  # Free-stream pressure (Bar)
        "T1": validate_input(t1_entry.get(), 216.65, 271.65),  # Free-stream temperature (K)
        "M1": validate_input(m1_entry.get(), 1, 6),  # Flight Mach number
        "Ms": validate_input(ms_entry.get(), 1, 10),  # Normal shock strength
        "M2": validate_input(m2_entry.get(), 0, 1),  # Burner entry Mach number
        "Tb": validate_input(tb_entry.get(), 1500, 2000),  # Burner temperature (K)
        "Thrust": validate_input(thrust_entry.get(), 0, 1e6),  # Required thrust (N)
    }
    
    if all(v is not None for v in values.values()):
        # Call ramjet calculations
        result = ramjet.calculations(
            values["P1"], values["T1"], values["M1"], values["Ms"],
            values["M2"], values["Tb"], values["Thrust"]
        )
        
        # Display results
        messagebox.showinfo("Calculation Results", 
                            f"A1: {result[0]:.4f}\n"
                            f"AC1: {result[1]:.4f}\n"
                            f"A2: {result[2]:.4f}\n"
                            f"AC2: {result[3]:.4f}\n"
                            f"A4: {result[4]:.4f}\n"
                            f"Thermal Efficiency: {result[5] * 100:.2f}%\n"
                            f"Propulsive Efficiency: {result[6] * 100:.2f}%")
        
        # Call the plotting function
        plot_ramjet_performance(values["P1"], values["T1"], values["M1"], values["Ms"],
                                values["M2"], values["Tb"], values["Thrust"])

# GUI Setup
root = tk.Tk()
root.title("Ramjet Input GUI")

fields = [
    ("Free-Stream Pressure (Bar) [0.025 - 0.4854]", "P1"),
    ("Free-Stream Temperature (K) [216.65 - 271.65]", "T1"),
    ("Flight Mach Number [1 - 6]", "M1"),
    ("Normal Shock Strength (>1, prevents inlet unstart)", "Ms"),
    ("Burner Entry Mach Number [0 - 1]", "M2"),
    ("Burner Temperature (K) [1500 - 2000]", "Tb"),
    ("Thrust (N) (>0, required thrust)", "Thrust")
]

entries = {}
for idx, (label, key) in enumerate(fields):
    tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky='w')
    entry = tk.Entry(root)
    entry.grid(row=idx, column=1, padx=10, pady=5)
    entries[key] = entry

p1_entry = entries["P1"]
t1_entry = entries["T1"]
m1_entry = entries["M1"]
ms_entry = entries["Ms"]
m2_entry = entries["M2"]
tb_entry = entries["Tb"]
thrust_entry = entries["Thrust"]

# Submit Button
tk.Button(root, text="Submit", command=submit).grid(row=len(fields), column=0, columnspan=2, pady=10)

# root.mainloop()  # Uncomment this when running the GUI
