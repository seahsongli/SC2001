# Comparison count vs. threshold values

import sys
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt


def read_data_from_stdin():
    thresholds = []
    comparison_counts = []

    # Read data from stdin
    for line in sys.stdin:
        try:
            # Expecting lines in format: <input_size>\t<comparison_count>
            threshold, comparison_count = map(int, line.split())
            if threshold == -1 and comparison_count == -1:
                break
            thresholds.append(threshold)
            comparison_counts.append(comparison_count)
        except ValueError:
            # Skip invalid lines
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return thresholds, comparison_counts


def plot_t_graph(thresholds, comparison_counts, ex):
    output_file = f"threshold_graph1e{ex}.png"
    # Convert to numpy arrays for numerical operations
    thresholds = np.array(thresholds)
    comparison_counts = np.array(comparison_counts)

    # Apply Gaussian smoothing to create a smooth line
    smoothed_counts = comparison_counts

    plt.figure(figsize=(10, 6))

    min_threshold = 0
    min_comparison = 0x7FFF_FFFF

    for i, t in enumerate(smoothed_counts):
        if t < min_comparison:
            min_comparison = t
            min_threshold = thresholds[i]

    plt.scatter(min_threshold, min_comparison, color="r", zorder=5)
    plt.text(
        min_threshold,
        min_comparison,
        f"S = {min_threshold}, cmpcnt = {min_comparison}",
        fontsize=12,
        ha="left",
        va="bottom",
        color="black",
    )

    plt.errorbar(
        thresholds,
        smoothed_counts,
        fmt="-",
        color="b",
        capsize=3,
        label="Comparison Count",
    )
    plt.xlabel("Threshold (S)")
    plt.ylabel("Comparison Count")
    plt.title(f"Comparison Count vs. Threshold (n = 1E+{ex})")
    plt.grid(True)
    plt.legend()

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the plot as an image file
    plt.savefig(output_file)
    plt.show()


def main():
    # Read data from stdin
    thresholds, comparison_counts = read_data_from_stdin()

    # Plot the graph and save it as an image
    plot_t_graph(thresholds, comparison_counts, 3)

    thresholds, comparison_counts = read_data_from_stdin()
    plot_t_graph(thresholds, comparison_counts, 4)
    thresholds, comparison_counts = read_data_from_stdin()
    plot_t_graph(thresholds, comparison_counts, 5)
    thresholds, comparison_counts = read_data_from_stdin()
    plot_t_graph(thresholds, comparison_counts, 6)
    thresholds, comparison_counts = read_data_from_stdin()
    plot_t_graph(thresholds, comparison_counts, 7)


if __name__ == "__main__":
    main()
