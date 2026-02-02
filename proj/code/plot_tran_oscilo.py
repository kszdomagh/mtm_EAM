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
        
        plt.figure(figsize=(10, 6))
        
        plt.plot(df['Time'], df['CH1'], label='Uzyskany przebieg', color='tab:red', linewidth=1, alpha=0.5)
        plt.plot(df['Time'], df['CH1_Avg'], label='Przebieg po uśrednianiu', color='tab:blue', linewidth=1.5)
        
        a = 0.84
        b = 1.69
        plt.axvline(a, color='tab:green', linestyle=':')
        plt.axvline(b, color='tab:green', linestyle=':')
        

        y_height = 6
        plt.annotate('', xy=(b, y_height), xytext=(a, y_height), arrowprops=dict(arrowstyle='<->', color='tab:green', lw=1.5))
        

        delta_t = b - a
        bpm = 60 / delta_t
        
        plt.text((a + b) / 2, y_height + 0.2, f'Δt = {delta_t:.2f}s\n{bpm:.1f} BPM', ha='center', va='bottom', fontsize=10, fontweight='bold', color='tab:green')


        plt.title('Pomiar EKG', fontsize=14)
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

plot_oscilloscope_file('../data/pomiary_ekg/Newfile7.csv')