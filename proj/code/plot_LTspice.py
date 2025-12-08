import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# --- Wczytanie danych ---
freqs = []
mags = []
phases = []

with open("../data/BP1_LTspice_AC.txt", "r", encoding="latin-1") as f:
    for line in f:
        m = re.match(r"([\deE\+\-\.]+)\s+\(([\-\d\.eE\+]+)dB,([\-\d\.eE\+]+)[°º]\)", line.strip())
        if m:
            freqs.append(float(m.group(1)))
            mags.append(float(m.group(2)))
            phases.append(float(m.group(3)))

# --- Funkcja znajdowania punktów -dB ---
def find_db_points(freq, mag20db, drop_db):
    freq = np.array(freq)
    mag20db = np.array(mag20db)

    peak = np.max(mag20db)
    th = peak - drop_db

    diff = mag20db - th
    crossings = np.where(np.diff(np.sign(diff)))[0]

    points = []
    for i in crossings:
        x1, x2 = freq[i], freq[i+1]
        y1, y2 = diff[i], diff[i+1]
        x_cross = x1 + (x2 - x1) * (-y1) / (y2 - y1)
        points.append(x_cross)

    return points

# --- Funkcja do zaokrąglania do 3 cyfr znaczących ---
def sig_figs(x, sig=3):
    if x == 0:
        return 0
    else:
        from math import log10, floor
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

# --- Funkcja do ładnego formatowania częstotliwości ---
def format_freq(f):
    f_rounded = sig_figs(f, 3)
    if f_rounded >= 1e6:
        return f"{f_rounded/1e6} MHz"
    elif f_rounded >= 1e3:
        return f"{f_rounded/1e3} kHz"
    else:
        return f"{f_rounded} Hz"

# --- Konwersja na numpy ---
freqs = np.array(freqs)
mags = np.array(mags)
phases = np.array(phases)

# --- Znalezienie punktów -3 dB ---
drop_db = 3
f3db = find_db_points(freqs, mags, drop_db)
print("3 dB points:", [format_freq(f) for f in f3db])

# --- Wykres ---
plt.figure(figsize=(7,4))
plt.semilogx(freqs, mags, label="Wzmocnienie filtru", color="tab:blue")

plt.title("Symulowana charakterystyka filtru pasmowo-przepustowego")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wzmocnienie [dB]")
plt.grid(True, which="both", ls="--")

plt.xlim(min(freqs), 4e6)
plt.ylim(-30, 50)

# Formatter osi X
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='Hz'))

# Linia -3 dB
peak = np.max(mags)
plt.axhline(peak - drop_db, color="red", linestyle="-.", label=f"poziom -{drop_db} dB")

# Linie pionowe dla punktów -3 dB z legendą
for i, f in enumerate(f3db):
    label = f"Częstotliwość graniczna {i+1}: {format_freq(f)}"
    plt.axvline(f, color="tab:green", linestyle="-", label=label)

plt.legend()
plt.show()
