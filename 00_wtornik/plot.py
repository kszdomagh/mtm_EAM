"""
Created on Mon Oct 27 14:40:59 2025

@author: kszdom


ELEKTRONICZNA APARATURA MEDYCZNA - WYKRESY
"""



import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("oscilo_csv/sim2.csv", skiprows=2, header=None)

data = df.values.flatten()

# Split into pairs
time = data[0::2]
voltage = data[1::2]


# Plot


plt.plot(time, voltage, marker='o')
plt.title("Voltage vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.show()





