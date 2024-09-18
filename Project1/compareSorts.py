import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from matplotlib.ticker import MaxNLocator


def read_data_from_stdin():
    input_sizes = []
    merge_sort_times = []
    insertion_sort_times = []

    for line in sys.stdin:
        try:
            # Expecting lines in format: <input_size>\t<merge_sort_time>\t<insertion_sort_time>
            input_size, merge_time, insertion_time = map(float, line.split())
            input_sizes.append(int(input_size))
            merge_sort_times.append(merge_time)
            insertion_sort_times.append(insertion_time)
        except ValueError:
            # Skip invalid lines
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return input_sizes, merge_sort_times, insertion_sort_times


def find_intersection_point(input_sizes, merge_times, insertion_times):
    for i in range(len(input_sizes)):
        if merge_times[i] < insertion_times[i]:
            return input_sizes[i], merge_times[i]
    return None, None  # In case no intersection is found


def plot_graph(
    input_sizes, merge_sort_times, insertion_sort_times, output_file="output_graph.png"
):
    input_sizes = np.array(input_sizes)
    merge_sort_times = np.array(merge_sort_times)
    insertion_sort_times = np.array(insertion_sort_times)

    # Apply Gaussian smoothing for better visualization (optional)
    smoothed_merge_times = gaussian_filter1d(merge_sort_times, sigma=2)
    smoothed_insertion_times = gaussian_filter1d(insertion_sort_times, sigma=2)

    # Find the intersection point
    intersection_n, intersection_time = find_intersection_point(
        input_sizes, smoothed_merge_times, smoothed_insertion_times
    )

    plt.figure(figsize=(10, 6))

    # Plot merge sort and insertion sort runtimes
    plt.plot(
        input_sizes,
        smoothed_merge_times,
        label="Merge Sort",
        color="b",
    )
    plt.plot(
        input_sizes,
        smoothed_insertion_times,
        label="Insertion Sort",
        color="r",
    )

    # Highlight the intersection point if found
    if intersection_n is not None:
        plt.scatter(intersection_n, intersection_time, color="g", zorder=5)
        plt.text(
            intersection_n,
            intersection_time,
            f"n = {intersection_n}",
            fontsize=12,
            ha="left",
            va="bottom",
            color="black",
        )

    plt.xlabel("Input Size (n)")
    plt.ylabel("Run Time (ms)")
    plt.title("Merge Sort vs. Insertion Sort Run Time")
    plt.grid(True)
    plt.legend()

    # Force integer values on x-axis
    plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the plot as an image file
    plt.savefig(output_file)
    plt.show()


def main():
    # Read data from stdin
    input_sizes, merge_sort_times, insertion_sort_times = read_data_from_stdin()

    # Plot the graph and save it as an image
    plot_graph(input_sizes, merge_sort_times, insertion_sort_times)


if __name__ == "__main__":
    main()
