import tkinter as tk
from tkinter import messagebox
import ramjet  # Import the ramjet function

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
        "P1": validate_input(p1_entry.get(), 0.025, 0.4854),  # Free-stream pressure (0.025 to 0.4854 Bar)
        "T1": validate_input(t1_entry.get(), 216.65, 271.65),  # Free-stream temperature (216.65 to 271.65 K)
        "M1": validate_input(m1_entry.get(), 1, 6),  # Flight Mach number (1 to 6)
        "Ms": validate_input(ms_entry.get(), 1, float('inf')),  # Normal shock strength (>1 to prevent inlet unstart)
        "M2": validate_input(m2_entry.get(), 0, 1),  # Burner entry Mach number (0 to 1)
        "Tb": validate_input(tb_entry.get(), 1500, 2000),  # Burner temperature (1500 to 2000 K, limited by materials)
        "Thrust": validate_input(thrust_entry.get(), 0, float('inf')),  # Required thrust (>0)
    }
    if all(v is not None for v in values.values()):
        result = ramjet.calculations(
            values["P1"], values["T1"], values["M1"], values["Ms"],
            values["M2"], values["Tb"], values["Thrust"]
        )
        messagebox.showinfo("Calculation Results", f"A1: {result[0]}\nAC1: {result[1]}\nA2: {result[2]}\nAC2: {result[3]}\nA4: {result[4]}\nThermal Efficiency: {result[5]}\nPropulsive Efficiency: {result[6]}")

# Create GUI window
root = tk.Tk()
root.title("Ramjet Input GUI")

# Labels and Entry Fields
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

#root.mainloop()  # Start the GUI
