# Comparison count vs. input size (hybrid sort)

import sys
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


def read_data_from_stdin():
    input_sizes = []
    comparison_counts = []

    # Read data from stdin
    for line in sys.stdin:
        try:
            # Expecting lines in format: <input_size>\t<comparison_count>
            input_size, comparison_count = map(int, line.split())
            input_sizes.append(input_size)
            comparison_counts.append(comparison_count)
        except ValueError:
            # Skip invalid lines
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return input_sizes, comparison_counts


def plot_h_graph(input_sizes, comparison_counts, output_file="hybrid_cmps_graph.png"):
    # Convert to numpy arrays for numerical operations
    input_sizes = np.array(input_sizes)
    comparison_counts = np.array(comparison_counts)

    # Apply Gaussian smoothing to create a smooth line
    smoothed_counts = gaussian_filter1d(comparison_counts, sigma=2)

    # Calculate n * log(n) for each input size
    n_log_n = 3 * input_sizes * np.log(input_sizes)

    plt.figure(figsize=(10, 6))

    # Plot the n * log(n) curve
    plt.plot(input_sizes, n_log_n, label=r"knlog(n), k = 3", linestyle="--", color="r")

    # Plot the smoothed line with error bars
    plt.errorbar(
        input_sizes,
        smoothed_counts,
        fmt="-",
        color="b",
        capsize=3,
        label="Comparison Count",
    )
    plt.xlabel("input size (n)")
    plt.ylabel("Comparison Count")
    plt.title("Comparison Count vs. Input Size")
    plt.yscale("log")
    plt.grid(True)
    plt.legend()

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the plot as an image file
    plt.savefig(output_file)
    plt.show()


def main():
    # Read data from stdin
    input_sizes, comparison_counts = read_data_from_stdin()

    # Plot the graph and save it as an image
    plot_h_graph(input_sizes, comparison_counts)


if __name__ == "__main__":
    main()
