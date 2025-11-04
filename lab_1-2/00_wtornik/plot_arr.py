"""
Created on Mon Oct 27 14:40:59 2025

@author: kszdom


ELEKTRONICZNA APARATURA MEDYCZNA - WYKRESY Z ARRAYA
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import EngFormatter

voltage_out = [
    9.41, 9.3, -9.08, -8.65, -8.12, -7.51, -6.99, -6.44, -5.95, -5.39,
    -4.92, -4.44, -4.01, -3.56, -3.04, -2.5, -1.98, -1.54, -0.909, -0.374,
    -0.002, 0.602, 1.01, 1.51, 2.02, 2.53, 2.93, 3.43, 4.11, 4.61,
    5.11, 5.46, 5.96, 6.49, 7.02, 7.55, 8.08, 8.65, 9.14, 9.65, 9.67, 
]
voltage_in =  np.arange(-10, 10.5, 0.5)

voltage_ideal = np.arange(-10, 10.5, 0.5)




#   WHAT TO PLOT
xaxis = voltage_in
yaxis = voltage_out

print(min(yaxis), max(yaxis))




#   OFFSET CALC
def draw_offset_line(xaxis, yaxis, **kwargs):
    # Find the index where xaxis is closest to 0
    idx = np.argmin(np.abs(xaxis))
    x = xaxis[idx]
    y = yaxis[idx]
    plt.plot([0, x], [0, y], **kwargs)
    offset = y - x
    print(f"OFFSET: {offset} V")





# PLOT
plt.figure(figsize=(6, 6))  # width=10, height=6 inches
plt.xlim(min(yaxis)-1, max(yaxis)+1)
plt.xlim(min(xaxis)-1, max(xaxis)+1)
draw_offset_line(xaxis, yaxis, color='purple', label='Offset')
plt.plot(xaxis, yaxis, marker='o', label='Zmierzona charakterystyka układu')
plt.plot(xaxis, voltage_ideal, color='grey', linestyle='--', label='idealna charakterystyka teoretyczna')
plt.title("Charakterystyka przejściowa (DC) układu wtórnika")
plt.xlabel("Napięcie wejściowe [V]")
plt.ylabel("Napięcie wyjściowe [V]")
plt.grid(True)

# VLINES
plt.axhline(max(yaxis), color='red', linestyle='--', label='Dodatnia linia zasilania')
plt.axhline(min(yaxis), color='green', linestyle='--', label='Ujemna linia zasilania')
plt.legend()


# 
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='V'))
ax.yaxis.set_major_formatter(EngFormatter(unit='V'))


plt.show()
