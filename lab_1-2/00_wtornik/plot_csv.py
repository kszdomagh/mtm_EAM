"""
Created on Mon Oct 27 14:40:59 2025

@author: kszdom


ELEKTRONICZNA APARATURA MEDYCZNA - WYKRESY Z CSV
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import EngFormatter  # <-- added

df = pd.read_csv("oscilo_csv/STEPwtornik5v.csv", skiprows=2, header=None)

data = df.values.flatten()



# Split into pairs
time = data[0::2]
voltage = data[1::2]

print(min(voltage), max(voltage))
print(len(voltage))

ten_perc_voltage = 0.5
ninety_perc_voltage = (5 - 0.1*5)




# --- plot
plt.figure(figsize=(6, 6))  # width=10, height=6 inches
plt.xlim(-1e-6, 1e-6)
plt.plot(time, voltage, marker='o')
plt.title("Odpowiedź układu wtórnika na skok napięciowy")
plt.xlabel("Czas [s]")
plt.ylabel("Napięcie [V]")
plt.grid(True)

# --- v line plotting
plt.axvline(-130e-9, color='red', linestyle='--', label='-130 ns')
plt.axvline(140e-9, color='green', linestyle='--', label='140ns')



# --- v line plotting
plt.axhline(ten_perc_voltage, color='pink', linestyle='--', label='90% napięcia skoku')
plt.axhline(ninety_perc_voltage, color='pink', linestyle='--', label='10% napięcia skoku')







plt.legend()


# --- automatic SI unit formatting ---
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='s'))
ax.yaxis.set_major_formatter(EngFormatter(unit='V'))


plt.show()
