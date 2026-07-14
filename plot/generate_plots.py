import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set font family to serif (similar to Times Roman in LaTeX)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['figure.titlesize'] = 12

def plot_results(csv_file, title, output_name, y_label="Average Execution Time (μs)", graph_label=None):
    """Generate a publication-quality plot with logarithmic y-axis scale.
    
    Per instructor directive: all graphs must use log scale.
    """
    df = pd.read_csv(csv_file)
    
    plt.figure(figsize=(8, 5))
    
    # Define styles for color and black-and-white readability
    styles = {
        'First': {'color': '#d62728', 'linestyle': '-', 'marker': 's', 'markevery': 10, 'label': 'First Element'},      # Red
        'Last': {'color': '#1f77b4', 'linestyle': '--', 'marker': 'o', 'markevery': 10, 'label': 'Last Element'},        # Blue
        'Middle': {'color': '#2ca02c', 'linestyle': ':', 'marker': '^', 'markevery': 10, 'label': 'Middle Element ⌊n/2⌋'}, # Green
        'Random': {'color': '#9467bd', 'linestyle': '-.', 'marker': 'x', 'markevery': 10, 'label': 'Random Element'}     # Purple
    }
    
    for strategy, style in styles.items():
        mean_col = strategy + '_mean'
        std_col = strategy + '_std'
        
        # Plot mean line
        plt.plot(df['Size'], df[mean_col], **style)
        
        # Plot shaded error band (mean ± std dev)
        # For log scale: clip lower band to 10% of mean to avoid visual artifacts
        lower_band = df[mean_col] - df[std_col]
        upper_band = df[mean_col] + df[std_col]
        lower_band_clipped = np.maximum(lower_band, df[mean_col] * 0.1)
        
        plt.fill_between(df['Size'], lower_band_clipped, upper_band, color=style['color'], alpha=0.12)
    
    # Always use log scale per instructor directive
    plt.yscale('log')
    
    plt.xlabel('Array Size (N)', fontsize=11)
    plt.ylabel(y_label + " (Log Scale)", fontsize=11)
    
    display_title = f"{graph_label}: {title}" if graph_label else title
    plt.title(display_title, fontsize=12, fontweight='bold', pad=10)
    plt.grid(True, which='both', color='lightgray', linestyle='--', linewidth=0.5)
    plt.legend(loc='best', frameon=True, edgecolor='black', fontsize=9)
    plt.tight_layout()
    plt.savefig(output_name, dpi=300, facecolor='white')
    plt.close()
    print(f"Saved plot: {output_name}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "..", "data")
    
    # Graph 1: Random arrays — Log scale (per instructor directive)
    plot_results(
        os.path.join(data_dir, "random_results.csv"), 
        "Quicksort Performance on Random Arrays", 
        os.path.join(script_dir, "plot_random.png"),
        graph_label="Graph 1"
    )
    # Graph 2A: Ascending arrays — Log scale
    plot_results(
        os.path.join(data_dir, "ascending_results.csv"), 
        "Quicksort Performance on Ascending Arrays", 
        os.path.join(script_dir, "plot_ascending.png"),
        graph_label="Graph 2A"
    )
    # Graph 2B: Descending arrays — Log scale
    plot_results(
        os.path.join(data_dir, "descending_results.csv"), 
        "Quicksort Performance on Descending Arrays", 
        os.path.join(script_dir, "plot_descending.png"),
        graph_label="Graph 2B"
    )
