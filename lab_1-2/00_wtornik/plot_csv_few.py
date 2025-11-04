import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import EngFormatter

# --- config ---
files = [
    "oscilo_csv/3_6v_supply.csv",
    "oscilo_csv/10v_supply.csv",
]

labels = ["3.6 V supply", "10 V supply"]
colors = ["blue", "red"]

plt.figure(figsize=(7, 5))

for file, label, color in zip(files, labels, colors):
    df = pd.read_csv(file, skiprows=2, header=None, usecols=[0, 1])
    df.columns = ["Time", "Voltage"]
    plt.plot(df["Time"], df["Voltage"], label=label, color=color, marker='o')


# --- formatting ---
plt.title("Wpływ zbyt niskiego zapięcia zasilania na układ wtórnika")
plt.xlabel("Czas [s]")
plt.ylabel("Napięcie [V]")
plt.legend(title="Zasilanie")
plt.grid(True)

# --- SI unit formatting ---
ax = plt.gca()
ax.xaxis.set_major_formatter(EngFormatter(unit='s'))
ax.yaxis.set_major_formatter(EngFormatter(unit='V'))

plt.show()
