import re
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter

# --- Data Containers ---
traces_v = []       # List of arrays for each step
traces_center = []
traces_freqs = []

current_freqs = []
current_v = []
current_center = []

# Regex: Handles scientific notation and ignores the degree symbol/phase
pattern = r"([\d.eE+-]+)\s+\(([\d.eE+-]+)dB"

try:
    with open("../data/FLIEGEsim_LTspice_AC.txt", "r", encoding="utf-16") as f:
        lines = f.readlines()
except:
    with open("../data/FLIEGEsim_LTspice_AC.txt", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

for line in lines:
    parts = re.findall(r"([-+]?[\d.]+(?:[eE][-+]?\d+)?)", line)
    
    if len(parts) >= 5:
        f_val = float(parts[0])
        v_val = float(parts[1])
        c_val = float(parts[3])

        # DETECTION LOGIC: If frequency drops, it means a new LTspice 'Step' started
        if current_freqs and f_val < current_freqs[-1]:
            traces_freqs.append(np.array(current_freqs))
            traces_v.append(np.array(current_v))
            traces_center.append(np.array(current_center))
            # Reset for next trace
            current_freqs, current_v, current_center = [], [], []

        current_freqs.append(f_val)
        current_v.append(v_val)
        current_center.append(c_val)

# Append the final trace
if current_freqs:
    traces_freqs.append(np.array(current_freqs))
    traces_v.append(np.array(current_v))
    traces_center.append(np.array(current_center))

# --- Plotting ---
plt.figure(figsize=(7,4))

plt.axvline(50, color='tab:red', linestyle='--', label='50Hz')

# Plot each trace separately to prevent wrap-around lines
for i in range(len(traces_freqs)):
    label_v = "Różne ustawienia potencjometru" if i == 0 else ""
    plt.semilogx(traces_freqs[i], traces_v[i], color="tab:blue", alpha=0.3, linewidth=1, label=label_v)

# Highlight the "Center" response (assuming it's the last one or you want to plot one specifically)
# If mag_center is the same for all steps, we just plot the last one found.
if traces_center:
    plt.semilogx(traces_freqs[-1], traces_center[-1], color="tab:green", 
                 alpha=1.0, linewidth=2.5, label="Potencjometr w środkowej pozycji")

# Formatting
plt.title("Odpowiedź częstotliwościowa filtru notch w architekturze FLIEGE")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")

plt.grid(True, which="both", ls="--", alpha=0.5)

ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='Hz'))

# Use the frequency range of the first trace for limits
if traces_freqs:
    plt.xlim(traces_freqs[0].min(), traces_freqs[0].max())

plt.grid(True, which="both", ls="--")
plt.legend(loc="lower left")
plt.xlim(20,100)
plt.ylim(-60,10)
plt.tight_layout()
plt.show()