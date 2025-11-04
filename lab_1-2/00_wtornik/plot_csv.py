"""
Created on Mon Oct 27 14:40:59 2025

@author: kszdom


ELEKTRONICZNA APARATURA MEDYCZNA - WYKRESY Z CSV
"""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import EngFormatter

df = pd.read_csv("oscilo_csv/STEPwtornik5v.csv", skiprows=2, header=None)

data = df.values.flatten()



# Split into pairs
time = data[0::2]
voltage = data[1::2]



# --- plot
plt.figure(figsize=(6, 4.5))  # width=10, height=6 inches
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
plt.axhline(10, color='pink', linestyle='--', label='90% napięcia skoku')






plt.legend()


# --- automatic SI unit formatting ---
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='s'))
ax.yaxis.set_major_formatter(EngFormatter(unit='V'))


plt.show()
