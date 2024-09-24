import sys
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt


def read_data_from_stdin():
    thresholds = []
    h_comparison_counts = []
    m_comparison_counts = []

    # Read data from stdin
    for line in sys.stdin:
        try:
            # Expecting lines in format: <threshold>\t<h_comparison_count>\t<m_comparison_count>
            threshold, h_comparison_count, m_comparison_count = map(int, line.split())
            thresholds.append(threshold)
            h_comparison_counts.append(h_comparison_count)
            m_comparison_counts.append(m_comparison_count)
        except ValueError:
            # Skip invalid lines
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return thresholds, h_comparison_counts, m_comparison_counts


def plot_diff_graph(
    thresholds, h_comparison_counts, m_comparison_counts, output_file="hmdiff_graph.png"
):
    # Convert to numpy arrays for numerical operations
    thresholds = np.array(thresholds)
    difference_counts = np.array(h_comparison_counts) - np.array(m_comparison_counts)

    # Apply Gaussian smoothing to create a smooth line
    difference_smoothed_counts = difference_counts

    plt.figure(figsize=(10, 6))

    # Plot the smoothed line with error bars
    plt.plot(
        thresholds,
        difference_smoothed_counts,
        color="b",
        label="h - m",
    )

    plt.xlabel("Threshold (S)")
    plt.ylabel("Comparison Count Difference (HybridSort - MergeSort)")
    plt.title("Comparison Count Difference vs. Threshold (n = 1E+6)")

    plt.grid(True)
    plt.legend()

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the plot as an image file
    plt.savefig(output_file)
    plt.show()


def main():
    # Read data from stdin
    thresholds, h_comparison_counts, m_comparison_counts = read_data_from_stdin()

    # Plot the graph and save it as an image
    plot_diff_graph(thresholds, h_comparison_counts, m_comparison_counts)


if __name__ == "__main__":
    main()
