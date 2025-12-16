import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter

# Frequencies in Hz
freq = np.array([
    0.01, 0.04, 0.07, 0.10, 0.15, 0.20, 0.25, 0.30, 0.33, 0.37,
    0.40, 0.43, 0.47, 0.50, 0.53, 0.57, 0.60, 0.63, 0.67, 0.70,
    0.73, 0.77, 0.80, 0.83, 0.87, 0.90, 0.93, 0.97, 1.00,
    3.00, 5.00, 7.00, 9.00, 10.00, 30.00, 70.00, 100.00,
    200.00, 230.00, 270.00, 300.00, 330.00, 370.00, 400.00,
    430.00, 470.00, 500.00, 530.00, 570.00, 600.00, 700.00,
    800.00, 900.00, 1000.00, 3000.00, 5000.00, 7000.00,
    9000.00, 11000.00, 13000.00, 30000.00, 50000.00, 100000.00
])

vin = np.array([
    0.10
] * len(freq))

vout = np.array([
    0.24, 0.94, 1.58, 2.22, 3.16, 4.12, 4.92, 5.60, 6.16, 6.40,
    6.80, 7.12, 7.44, 7.52, 7.84, 8.08, 8.24, 8.40, 8.64, 8.72,
    8.88, 9.04, 9.04, 9.12, 9.20, 9.30, 9.36, 9.36, 9.52,
    10.30, 10.50, 10.50, 10.50, 10.60, 10.80, 10.80, 10.60,
    9.80, 9.80, 9.20, 9.20, 8.60, 8.60, 8.20,
    8.20, 7.80, 7.60, 7.40, 7.00, 7.00, 6.20,
    6.00, 5.40, 5.00, 1.90, 1.20, 0.94,
    0.80, 0.68, 0.60, 0.42, 0.30, 0.26
])

# Convert to dB
gain_db = 20 * np.log10(vout/vin)

# PLOT
plt.figure(figsize=(8, 6))
plt.semilogx(freq, gain_db, marker='o', label='Zmierzona charakterystyka (AC) układu wtórnika')
plt.title("Charakterystyka częstotliwościowa układu (dB)")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Transmitrancja układu [dB]")
plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend()

# Format x-axis
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='Hz'))

plt.show()
