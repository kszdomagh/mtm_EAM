import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Wczytanie pliku ----
raw = pd.read_csv("100Hz.csv", header=None)

# Odczyt parametrów
start_time = float(raw.iloc[1, 2])       # Start
increment = float(raw.iloc[1, 3])        # Increment

# Dane zaczynają się od wiersza 2
df = raw.iloc[2:, :2]
df.columns = ["index", "ch1"]
df = df.apply(pd.to_numeric, errors="coerce").dropna()

# Generowanie czasu
df["time"] = start_time + df["index"] * increment
df["time_us"] = df["time"] * 1e6

# ---- Detekcja częstotliwości ----
ch = df["ch1"].values
t = df["time"].values

zero_crossings = np.where(np.diff(np.signbit(ch)))[0]

if len(zero_crossings) > 1:
    periods = np.diff(t[zero_crossings])
    avg_period = np.mean(periods)
    frequency = 1 / avg_period
    print(f"Estimated frequency: {frequency:.2f} Hz")
else:
    print("Not enough zero-crossings to estimate frequency.")

# ---- Wykres ----
plt.figure(figsize=(7, 4))  # width=10, height=6 inches

plt.plot(df["time_us"], df["ch1"], label="Sygnał na wyjściu układu całkującego", linestyle='--', color='r')

plt.xlim(min(df["time_us"]), max(df["time_us"]))
plt.xlabel("Time (µs)")
plt.ylabel("Napięcie [V]")
plt.title("Sygnał prostokątny o częstotliwoci 100 Hz podany na wejście układu")
plt.grid(True)
plt.legend(loc="lower right")
plt.tight_layout()
plt.show()
