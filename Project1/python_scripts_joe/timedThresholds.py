import sys
from matplotlib.ticker import MaxNLocator
import numpy as np
import matplotlib.pyplot as plt


def read_data_from_stdin():
    thresholds = []
    runtimes = []

    # Read data from stdin
    for line in sys.stdin:
        try:
            # Expecting lines in format: <threshold>\t<runtime>
            threshold, runtime = map(int, line.split())
            if threshold == -1 and runtime == -1:
                break
            thresholds.append(threshold)
            runtimes.append(runtime)
        except ValueError:
            # Skip invalid lines
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return thresholds, runtimes


def plot_diff_graph(thresholds, runtimes, ex):
    output_file = f"t_timed_graph1e{ex}.png"
    # Convert to numpy arrays for numerical operations
    thresholds = np.array(thresholds)
    runtimes = np.array(runtimes)
    smoothed_runtimes = runtimes  # gaussian_filter1d(runtimes, sigma=2)
    min_threshold = 0
    min_runtime = 0x7FFF_FFFF

    for i, t in enumerate(smoothed_runtimes):
        if t < min_runtime:
            min_runtime = t
            min_threshold = thresholds[i]

    plt.figure(figsize=(10, 6))

    # Plot the smoothed line with error bars
    plt.plot(
        thresholds,
        smoothed_runtimes,
        color="b",
        label="runtime",
    )

    plt.scatter(min_threshold, min_runtime, color="r", zorder=5)
    plt.text(
        min_threshold,
        min_runtime,
        f"S = {min_threshold}",
        fontsize=12,
        ha="left",
        va="bottom",
        color="black",
    )

    plt.xlabel("Threshold (S)")
    plt.ylabel("Runtime (us)")
    plt.title(f"Runtime vs. Threshold (n = 1E+{ex})")
    plt.grid(True)
    plt.legend()

    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the plot as an image file
    plt.savefig(output_file)
    plt.show()


def main():
    # Read data from stdin
    thresholds, runtimes = read_data_from_stdin()

    # Plot the graph and save it as an image
    plot_diff_graph(thresholds, runtimes, 3)

    thresholds, runtimes = read_data_from_stdin()
    plot_diff_graph(thresholds, runtimes, 4)
    thresholds, runtimes = read_data_from_stdin()
    plot_diff_graph(thresholds, runtimes, 5)
    thresholds, runtimes = read_data_from_stdin()
    plot_diff_graph(thresholds, runtimes, 6)
    thresholds, runtimes = read_data_from_stdin()
    plot_diff_graph(thresholds, runtimes, 7)


if __name__ == "__main__":
    main()
