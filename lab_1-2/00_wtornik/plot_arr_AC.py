import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter

# Frequencies in Hz
freq = [
    1, 10, 100, 1_000, 10_000, 100_000, 200_000, 600_000,
    1_000_000, 1_200_000, 1_400_000, 1_600_000, 1_800_000,
    2_000_000, 2_200_000, 2_400_000, 2_600_000, 2_800_000,
    3_000_000, 3_200_000, 3_400_000, 3_600_000, 3_800_000,
    4_000_000, 4_200_000, 4_400_000, 4_600_000, 4_800_000, 5_000_000
]

gain = [
    1.055, 1.07, 1.085, 1.06, 1.08, 1.08, 1.06, 1.1,
    1.16, 1.22, 1.28, 1.32, 1.34, 1.315, 1.18, 1.04,
    0.98, 0.84, 0.74, 0.66, 0.62, 0.56, 0.5, 0.46, 0.44,
    0.36, 0.3, 0.287, 0.284
]

# Convert to dB
gain_db = 20 * np.log10(gain)

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
