import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import os
from math import log10, floor # Wymagane dla sig_figs

# =========================================================================
# === DANE WEJŚCIOWE I KONFIGURACJA (DO EDYCJI) ===
# =========================================================================

# Ścieżka do pliku symulacji AC (np. z LTSpice)
SCIEZKA_SYMULACJI = "../data/BP2_LTspice_AC.txt" 

# Wymagany spadek wzmocnienia do znalezienia częstotliwości granicznych [dB]
DROP_DB = 6

# Frequency values (Hz)
freq_pomiary = np.array([
    0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.5, 2.0, 2.4, 2.7, 
    2.8, 2.9, 3.0, 5.0, 6.0, 10.0, 30.0, 50.0, 80.0, 100.0, 
    200.0, 250.0, 270.0, 300.0, 320.0, 350.0, 370.0, 390.0, 400.0, 410.0, 
    420.0, 430.0, 470.0, 500.0, 600.0, 800.0, 1000.0, 1400.0, 4000.0
])

# Input Voltage (Constant 3.0V based on the ratio calculations)
vin_pomiary = np.array([3.0] * len(freq_pomiary))

# Output Voltage values (Vpp)
vout_pomiary = np.array([
    0.72, 0.88, 1.02, 1.20, 1.38, 1.54, 2.12, 2.46, 2.74, 2.88,
    2.94, 3.04, 3.04, 3.06, 3.08, 3.10, 3.10, 3.08, 3.0, 3.0,
    2.94, 2.68, 2.56, 2.32, 2.20, 1.94, 1.83, 1.68, 1.62, 1.54,
    1.48, 1.42, 1.24, 1.10, 0.75, 0.43, 0.27, 0.14, 0.008
])
# =========================================================================
# === FUNKCJE POMOCNICZE ===
# =========================================================================

def sig_figs(x, sig=3):
    """Zaokrągla liczbę do podanej liczby cyfr znaczących."""
    if x == 0:
        return 0
    else:
        return round(x, sig - int(floor(log10(abs(x)))) - 1)

def format_freq(f):
    """Formatuje częstotliwość używając prefiksów inżynierskich (Hz, kHz, MHz)."""
    f_rounded = sig_figs(f, 3)
    if f_rounded >= 1e6:
        return f"{f_rounded/1e6} MHz"
    elif f_rounded >= 1e3:
        return f"{f_rounded/1e3} kHz"
    else:
        return f"{f_rounded} Hz"

def find_db_points(freq, mag20db, drop_db):
    """
    Znajduje częstotliwości, dla których wzmocnienie spadło o 'drop_db'
    względem wartości szczytowej (peak), używając interpolacji liniowej.
    """
    freq = np.array(freq)
    mag20db = np.array(mag20db)

    valid_data = np.isfinite(mag20db) & (freq > 0)
    freq_valid = freq[valid_data]
    mag20db_valid = mag20db[valid_data]
    
    if len(freq_valid) < 2:
        return []

    peak = np.max(mag20db_valid)
    th = peak - drop_db

    diff = mag20db_valid - th
    crossings = np.where(np.diff(np.sign(diff)))[0]

    points = []
    for i in crossings:
        x1, x2 = freq_valid[i], freq_valid[i+1]
        y1, y2 = diff[i], diff[i+1]
        
        # Interpolacja liniowa
        x_cross = x1 + (x2 - x1) * (-y1) / (y2 - y1)
        points.append(x_cross)

    return points


# =========================================================================
# === PRZETWARZANIE DANYCH ===
# =========================================================================

# --- 1. PRZETWARZANIE POMIARÓW ---
with np.errstate(divide='ignore', invalid='ignore'):
    gain_db_pomiary = 20 * np.log10(vout_pomiary / vin_pomiary)
    
valid_mask_pomiary = np.isfinite(gain_db_pomiary) & (freq_pomiary > 0)
freq_pomiary_valid = freq_pomiary[valid_mask_pomiary]
gain_db_pomiary_valid = gain_db_pomiary[valid_mask_pomiary]


# --- 2. PRZETWARZANIE SYMULACJI (Wczytywanie pliku) ---
freqs_sym = []
mags_sym = []

try:
    if not os.path.exists(SCIEZKA_SYMULACJI):
        raise FileNotFoundError(f"Plik symulacji nie znaleziony: {SCIEZKA_SYMULACJI}")
        
    with open(SCIEZKA_SYMULACJI, "r", encoding="latin-1") as f:
        for line in f:
            # Wzorzec dopasowuje: Częstotliwość (Wzmocnienie w dB, Faza w stopniach)
            m = re.match(r"([\deE\+\-\.]+)\s+\(([\-\d\.eE\+]+)dB,([\-\d\.eE\+]+)[°º]\)", line.strip())
            if m:
                freqs_sym.append(float(m.group(1)))
                mags_sym.append(float(m.group(2)))

    if not freqs_sym:
        print("OSTRZEŻENIE: W pliku symulacji nie znaleziono danych pasujących do wzorca.")
        raise ValueError("Brak danych AC.")
        
except (FileNotFoundError, ValueError) as e:
    print(f"BŁĄD: {e}")
    print("Użycie PRZYKŁADOWYCH danych symulacji do uruchomienia wykresu.")
    # PRZYKŁADOWE DANE
    freqs_sym = np.logspace(-1, 5, 200) 
    mags_sym = 20 * np.log10(10.0 / (1 + (freqs_sym/1000)**2)) 
    
freqs_sym = np.array(freqs_sym)
mags_sym = np.array(mags_sym)


# =========================================================================
# === ANALIZA I WYNIKI (Dla konsoli) ===
# =========================================================================

f3db_sym = find_db_points(freqs_sym, mags_sym, DROP_DB)
f3db_pomiary = find_db_points(freq_pomiary_valid, gain_db_pomiary_valid, DROP_DB)

print("\n--- Punkty -3 dB (Symulacja) ---")
if len(mags_sym) > 0:
    print("Wartość szczytowa symulacji: ", sig_figs(np.max(mags_sym), 4), " dB")
print(f"{DROP_DB} dB points:", [format_freq(f) for f in f3db_sym])

print("\n--- Punkty -3 dB (Pomiary) ---")
if len(gain_db_pomiary_valid) > 0:
    print("Wartość szczytowa pomiarów: ", sig_figs(np.max(gain_db_pomiary_valid), 4), " dB")
print(f"{DROP_DB} dB points:", [format_freq(f) for f in f3db_pomiary])


# =========================================================================
# === WIZUALIZACJA DANYCH (Wykres Bode) ===
# =========================================================================

plt.figure(figsize=(10, 8))

# --- WYKRES SYMULACJI ---
plt.semilogx(freqs_sym, mags_sym, 
             label="Symulacja", 
             color="tab:red", 
             linewidth=2)

# --- WYKRES POMIARÓW ---
plt.semilogx(freq_pomiary_valid, gain_db_pomiary_valid, 
             marker='o', linestyle='--', markersize=4, 
             label='Pomiary', 
             color="tab:blue")

# --- ZAZNACZENIE PUNKTÓW GRANICZNYCH (-3 dB) ---
if len(mags_sym) > 0:
    peak_sym = np.max(mags_sym)
    plt.axhline(peak_sym - DROP_DB, color="tab:orange", linestyle=":", linewidth=1, 
                label=f"Próg -{DROP_DB} dB (Symulacja)")
    for i, f in enumerate(f3db_sym):
        plt.axvline(f, color="tab:orange", linestyle="-.", linewidth=1, alpha=0.6)
        plt.plot(f, peak_sym - DROP_DB, 'o', color="tab:orange", markersize=6)

if len(gain_db_pomiary_valid) > 0:
    peak_pom = np.max(gain_db_pomiary_valid)
    plt.axhline(peak_pom - DROP_DB, color="tab:blue", linestyle=":", linewidth=1, 
                label=f"Próg -{DROP_DB} dB (Pomiary)")
    for i, f in enumerate(f3db_pomiary):
        plt.axvline(f, color="tab:blue", linestyle="-.", linewidth=1, alpha=0.6)
        plt.plot(f, peak_pom - DROP_DB, 'x', color="tab:blue", markersize=6, markeredgewidth=2)


# --- FORMATOWANIE WYKRESU ---
plt.title("Porównanie charakterystyk częstotliwościowych (AC) dla układu filtru pasmowo-przepustowego BP2")
plt.xlabel("Częstotliwość [Hz]")
plt.ylabel("Wzmocnienie / Transmitancja [dB]")
plt.grid(True, which="both", ls="--", lw=0.5)
plt.legend(loc='lower left', fontsize='small')

# Formatter osi X (EngFormatter)
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='Hz'))

# Automatyczne ustawienie limitów X
try:
    all_freqs = np.concatenate([freqs_sym[freqs_sym > 0], freq_pomiary_valid[freq_pomiary_valid > 0]])
    if len(all_freqs) > 0:
        min_freq = np.min(all_freqs)
        max_freq = np.max(all_freqs)
        plt.xlim(0.1, 5e3)
        plt.ylim(-30, 5)
except ValueError:
    pass # Pozostawienie domyślnych limitów, jeśli nie ma danych

plt.show()