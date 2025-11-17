import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import EngFormatter

# Frequencies in Hz
freq = [
    100, 1_000, 10_000, 12_000, 14_000, 16_000, 18_000, 20_000, 22_000, 24_000,
    26_000, 28_000, 30_000, 35_000, 40_000, 45_000, 46_000, 47_000, 48_000, 49_000,
    50_000, 55_000, 60_000, 65_000, 70_000, 75_000, 80_000, 85_000, 90_000, 95_000,
    100_000, 110_000, 120_000, 130_000, 140_000, 150_000, 160_000, 170_000, 180_000,
    190_000, 200_000, 225_000, 250_000, 275_000, 300_000, 350_000, 400_000, 500_000,
    600_000, 700_000, 900_000, 1_200_000, 3_000_000, 4_000_000
]

gain = [
    103.3333333, 104, 102.3333333, 101.3333333, 100, 99.33333333, 98.66666667, 
    97.33333333, 96, 95.33333333, 94, 92.66666667, 90.66666667, 88, 84.66666667, 
    80.66666667, 80, 79.33333333, 78.66666667, 78, 77.33333333, 74, 71.33333333, 
    68, 64.66666667, 62.66666667, 60, 57.33333333, 54.66666667, 52.66666667, 
    50.66666667, 48, 44.66666667, 39.33333333, 38.66666667, 36.66666667, 
    34.66666667, 33.33333333, 31.33333333, 30.66666667, 28.66666667, 25.33333333, 
    22.66666667, 21.33333333, 19.33333333, 16.66666667, 14.66666667, 11.33333333, 
    9.233333333, 7.733333333, 5.866666667, 4.416666667, 1.333333333, 1.066666667
]

# Convert to dB
gain_db = 20 * np.log10(gain)

# Oblicz -3dB względem maksymalnej wartości
gain_3db = max(gain_db) - 3

# Znajdź indeks najbliższej wartości w gain_db do -3dB
idx_3db = (np.abs(gain_db - gain_3db)).argmin()
freq_3db = freq[idx_3db]

# PLOT
plt.figure(figsize=(8, 6))
plt.semilogx(freq, gain_db, marker='o', label='Zmierzona charakterystyka układu wzmacniacza nieodwracającego')
plt.title("Charakterystyka częstotliwościowa (AC) układu wzmacniacza nieodwracającego")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Transmitrancja układu [dB]")

# Linie -3dB
plt.axhline(gain_3db, color='red', linestyle='--', label='-3dB')
plt.axvline(freq_3db, color='red', linestyle='--', label=f'Częst. -3dB ≈ {freq_3db/1000:.1f} kHz')

plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend()

# Format x-axis
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='Hz'))

plt.show()
