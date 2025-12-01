import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Wczytanie pliku ----
df = pd.read_csv("NewFile7.csv", skiprows=1)
df = df.iloc[:, :3]
df.columns = ["time", "ch1", "ch2"]
df = df.apply(pd.to_numeric, errors="coerce").dropna()

# ---- Skalowanie czasu ----
df["time_us"] = df["time"] * 1e6

# ---- Obliczanie częstotliwości z CH1 ----
# Szukanie przejść przez zero (zbocze narastające)
ch = df["ch1"].values
t = df["time"].values  # w sekundach

zero_crossings = np.where(np.diff(np.signbit(ch)))[0]

if len(zero_crossings) > 1:
    # bierzemy odstęp czasu między kolejnymi zboczami
    periods = np.diff(t[zero_crossings])
    avg_period = np.mean(periods)
    frequency = 1 / avg_period
    print(f"Estimated frequency: {frequency:.2f} Hz")
else:
    print("Not enough zero-crossings to estimate frequency.")

# ---- Wykres ----
plt.figure(figsize=(9,4))
plt.plot(df["time_us"], df["ch1"], label="CH1")
plt.plot(df["time_us"], df["ch2"], label="CH2")

plt.xlabel("Time (µs)")
plt.ylabel("Voltage (V)")
plt.title("Waveform from CSV")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
