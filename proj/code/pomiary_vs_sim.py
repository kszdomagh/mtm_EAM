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
SCIEZKA_SYMULACJI = "../data/BP1_LTspice_AC.txt" 

# Wymagany spadek wzmocnienia do znalezienia częstotliwości granicznych [dB]
DROP_DB = 3 

# --- DANE POMIAROWE (Arraye Vin/Vout/Freq) ---
# Frequencies in Hz
freq_pomiary = np.array([
    0.01, 0.04, 0.07, 0.10, 0.15, 0.20, 0.25, 0.30, 0.33, 0.37,
    0.40, 0.43, 0.47, 0.50, 0.53, 0.57, 0.60, 0.63, 0.67, 0.70,
    0.73, 0.77, 0.80, 0.83, 0.87, 0.90, 0.93, 0.97, 1.00,
    3.00, 5.00, 7.00, 9.00, 10.00, 30.00, 70.00, 100.00,
    200.00, 230.00, 270.00, 300.00, 330.00, 370.00, 400.00,
    430.00, 470.00, 500.00, 530.00, 570.00, 600.00, 700.00,
    800.00, 900.00, 1000.00, 3000.00, 5000.00, 7000.00,
    9000.00, 11000.00, 13000.00, 30000.00, 50000.00, 100000.00
])
vin_pomiary = np.array([0.10] * len(freq_pomiary))
vout_pomiary = np.array([
    0.24, 0.94, 1.58, 2.22, 3.16, 4.12, 4.92, 5.60, 6.16, 6.40,
    6.80, 7.12, 7.44, 7.52, 7.84, 8.08, 8.24, 8.40, 8.64, 8.72,
    8.88, 9.04, 9.04, 9.12, 9.20, 9.30, 9.36, 9.36, 9.52,
    10.30, 10.50, 10.50, 10.50, 10.60, 10.80, 10.80, 10.60,
    9.80, 9.80, 9.20, 9.20, 8.60, 8.60, 8.20,
    8.20, 7.80, 7.60, 7.40, 7.00, 7.00, 6.20,
    6.00, 5.40, 5.00, 1.90, 1.20, 0.94,
    0.80, 0.68, 0.60, 0.42, 0.30, 0.26
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
plt.title("Porównanie charakterystyk częstotliwościowych (AC) dla układu filtru pasmowo-przepustowego BP1")
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
        plt.xlim(10e-3, 1e6)
        plt.ylim(-10, 50)
except ValueError:
    pass # Pozostawienie domyślnych limitów, jeśli nie ma danych

plt.show()