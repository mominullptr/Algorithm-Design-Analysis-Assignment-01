import os
import pandas as pd
import matplotlib.pyplot as plt

# Set font family to serif (similar to Times Roman in LaTeX)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.titlesize'] = 12

def plot_results(csv_file, title, output_name, y_label="Average Execution Time (μs)"):
    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(6, 4))
    
    # Define styles for black and white readability
    styles = {
        'First': {'color': '#d62728', 'linestyle': '-', 'marker': 's', 'markevery': 10, 'label': 'First Element'}, # Red
        'Last': {'color': '#1f77b4', 'linestyle': '--', 'marker': 'o', 'markevery': 10, 'label': 'Last Element'}, # Blue
        'Middle': {'color': '#2ca02c', 'linestyle': ':', 'marker': '^', 'markevery': 10, 'label': 'Middle Element ⌊n/2⌋'}, # Green
        'Random': {'color': '#9467bd', 'linestyle': '-.', 'marker': 'x', 'markevery': 10, 'label': 'Random Element'} # Purple
    }
    
    for strategy, style in styles.items():
        plt.plot(df['Size'], df[strategy], **style)
        
    plt.xlabel('Array Size ($N$)', fontsize=10)
    plt.ylabel(y_label, fontsize=10)
    plt.title(title, fontsize=11, fontweight='bold', pad=10)
    plt.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.5)
    plt.legend(loc='best', frameon=True, edgecolor='black', fontsize=9)
    plt.tight_layout()
    plt.savefig(output_name, dpi=300, facecolor='white')
    plt.close()
    print(f"Saved plot: {output_name}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    
    plot_results(
        os.path.join(data_dir, "random_results.csv"), 
        "Quicksort Performance on Random Arrays", 
        os.path.join(script_dir, "plot_random.png")
    )
    plot_results(
        os.path.join(data_dir, "ascending_results.csv"), 
        "Quicksort Performance on Ascending Arrays", 
        os.path.join(script_dir, "plot_ascending.png")
    )
    plot_results(
        os.path.join(data_dir, "descending_results.csv"), 
        "Quicksort Performance on Descending Arrays", 
        os.path.join(script_dir, "plot_descending.png")
    )

