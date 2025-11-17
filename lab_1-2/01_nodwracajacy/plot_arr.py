"""
Created on Mon Oct 27 14:40:59 2025

@author: kszdom


ELEKTRONICZNA APARATURA MEDYCZNA - WYKRESY Z ARRAYA
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.ticker import EngFormatter

voltage_in = [
    -10, -9.5, -9, -8.5, -8, -7.5, -7, -6.5, -6, -5.5,
    -5, -4.5, -4, -3.5, -3, -2.5, -2, -1.5, -1, -0.5,
    -0.4, -0.1, -0.090, -0.080, -0.070, -0.060, -0.050, -0.040,
    -0.030, -0.020, -0.010, 0, 0.01, 0.02, 0.03, 0.04,
    0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.2, 0.5, 1,
    1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6,
    6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10
]

voltage_out = [
    -10, -10, -10, -10, -10, -10, -10, -10, -10, -10,
    -10, -10, -10, -10, -10, -10, -10, -10, -10, -10,
    -10, -10, -9.15, -8.16, -7.12, -6.16, -5.12, -4.08,
    -3.04, -2.00, -0.96, -0.08, 0.96, 2.00, 3.04, 4.08,
    5.04, 6.08, 7.12, 8.16, 9.20, 9.76, 9.92, 9.92, 9.92,
    9.92, 9.92, 9.92, 9.93, 9.93, 9.93, 9.92, 9.92, 9.94, 9.92,
    9.92, 9.92, 9.92, 9.95, 9.95, 9.96, 9.92, 9.92
]


voltage_in_ideal = np.arange(-0.1, 0.1, 0.01)

voltage_out_ideal = np.arange(-10, 10, 1)









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
plt.figure(figsize=(7, 7))  # width=10, height=6 inches
plt.xlim(min(yaxis)-1, max(yaxis)+1)
plt.xlim(min(xaxis)-1, max(xaxis)+1)
draw_offset_line(xaxis, yaxis, color='purple', label='Offset')
plt.plot(xaxis, yaxis, marker='o', label='Zmierzona charakterystyka układu')

plt.plot(voltage_in_ideal, voltage_out_ideal, linestyle='--', color='black', label='Idealna charakerystyka wzmacniacza')
# plt.plot(xaxis, voltage_ideal, color='grey', linestyle='--', label='idealna charakterystyka teoretyczna')
plt.title("Charakterystyka przejściowa (DC) układu wzmacniacza nieodwracającego")
plt.xlabel("Napięcie wejściowe [V]")
plt.ylabel("Napięcie wyjściowe [V]")
plt.grid(True)

# VLINES
plt.axhline(max(yaxis), color='red', linestyle='--', label='Dodatnia linia zasilania')
plt.axhline(min(yaxis), color='green', linestyle='--', label='Ujemna linia zasilania')
plt.legend()


# 
plt.xlim(-0.3, 0.3)
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='V'))
ax.yaxis.set_major_formatter(EngFormatter(unit='V'))


plt.show()
