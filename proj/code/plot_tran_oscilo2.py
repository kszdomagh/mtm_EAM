import pandas as pd
import matplotlib.pyplot as plt

def plot_oscilloscope_file(filename):
    try:

        with open(filename, 'r') as f:
            lines = f.readlines()
            header_values = lines[1].strip().split(',')
            increment_val = float(header_values[3])
        
        df = pd.read_csv(filename, skiprows=2, names=['Sequence', 'CH1', 'CH2', 'Empty'])
        df = df[['Sequence', 'CH1']]       
        df['Time'] = df['Sequence'] * increment_val
        df['CH1_Avg'] = df['CH1'].rolling(window=4).mean()
        
        plt.figure(figsize=(10, 3))
        
        plt.plot(df['Time'], df['CH1'], label='Przebieg na wyjściu', color='tab:red', linewidth=1)
        plt.title('Pomiar EKG - zbliżenie w czasie', fontsize=14)
        plt.xlim(min(df['Time']), max(df['Time']))
        plt.xlabel('Time [s]', fontsize=12)
        plt.ylabel('Voltage [V]', fontsize=12)
        plt.grid(linestyle='--', linewidth=0.5, alpha=0.5)
        plt.legend(loc='upper right')
        
        plt.style.use('default')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error: {e}")

plot_oscilloscope_file('../data/pomiary_ekg/Newfile5.csv')