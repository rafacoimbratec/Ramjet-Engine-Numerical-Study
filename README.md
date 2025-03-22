# 🚀 Ramjet Engine Simulation

This program was developed under the course Space Launchers from Instituto Superior Técnico.
A Python-based simulation tool to model the performance of a ramjet engine, including the evaluation of key geometric parameters, thermal and propulsive efficiency, and parametric analysis across design conditions.

## 🔧 Features

- Computes **engine station parameters** (areas, temperatures, pressures)
- Supports **isentropic & shock flow analysis**
- Calculates:
  - Thermal efficiency (based on Brayton cycle assumptions)
  - Propulsive efficiency
  - Total efficiency
- Plots:
  - Temperature and pressure variation along the engine
  - Temperature vs. entropy change ($T$–$\Delta s$ diagram)
- Built-in **parametric study**:
  - Vary Mach number, burner temperature, shock strength, thrust, etc.
- Easy-to-use **menu interface** via terminal

## 📂 Project Structure

```
Ramjet_Program/
│
├── ramjet.py             # Core calculations
├── main.py               # Menu + plotting + parametric study
├── ramjet_stations.png   # Engine station diagram
└── README.md             # You're here 🚀
```

## ▶️ How to Run

```bash
python main.py
```

Then choose from the terminal menu:
- Option 1: Analyze a custom design case by entering engine parameters
- Option 2: Run a parametric study across a chosen variable - Check the code for what are the constant values of the remaining variables

## 🔢 Example

```
Enter your choice [1 or 2]: 1
Free-stream Pressure P1 (Pa): 70000
Free-stream Temperature T1 (K): 210
Flight Mach Number M1: 3
...
```

Results are printed and plotted automatically.

### Dependencies:
- `numpy`
- `matplotlib`

## 📸 Visual Overview

The diagram below illustrates engine stations used in the calculations:

- 1: Inlet
- T1: After isentropic compression
- x/y: Before and after shock
- 2: Burner entry
- b: Burner exit
- T2: Nozzle throat
- 4: Exhaust
(ramjet_stations.png)
## 👨‍💻 Author

Rafael [@rafacoimbratec]  
---

📘 Inspired by **Aircraft Propulsion** by Saeed Farokhi (2nd Ed.)




