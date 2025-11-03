"""
Created on Mon Oct 27 14:40:59 2025

@author: kszdom


ELEKTRONICZNA APARATURA MEDYCZNA - WYKRESY
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import EngFormatter  # <-- added

df = pd.read_csv("oscilo_csv/sim2.csv", skiprows=2, header=None)

data = df.values.flatten()



# Split into pairs
time = data[0::2]
voltage = data[1::2]

print(min(voltage), max(voltage))



# --- plot
plt.figure(figsize=(10, 6))  # width=10, height=6 inches
plt.xlim(-2e-6, 2e-6)
plt.plot(time, voltage, marker='o')
plt.title("Odpowiedź ukłądu wtórnika na skok napięciowy")
plt.xlabel("Czas (s)")
plt.ylabel("Napięcie (V)")
plt.grid(True)

# --- v line plotting
plt.axvline(-200e-9, color='red', linestyle='--', label='a')
plt.axvline(300e-9, color='green', linestyle='--', label='b')
plt.legend()


# --- automatic SI unit formatting ---
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='s'))
ax.yaxis.set_major_formatter(EngFormatter(unit='V'))


plt.show()
