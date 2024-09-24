import sys
import numpy as np
import matplotlib.pyplot as plt


def read_data_from_stdin():
    hybrid_sort_times = []
    merge_sort_times = []

    # Reading runtime data from stdin, expecting multiple runs per input size
    for line in sys.stdin:
        try:
            # Expecting lines in format: <hybrid_sort_time>\t<merge_sort_time>
            hybrid_time, merge_time = map(int, line.split())
            hybrid_sort_times.append(hybrid_time)
            merge_sort_times.append(merge_time)
        except ValueError:
            # Skip invalid lines
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return hybrid_sort_times, merge_sort_times


def plot_boxplot(hybrid_sort_times, merge_sort_times, output_file="boxplot_graph.png"):
    plt.figure(figsize=(10, 6))

    # Create a boxplot comparing Hybrid Sort and Merge Sort
    data = [merge_sort_times, hybrid_sort_times]
    plt.boxplot(
        data,
        labels=["Merge Sort", "Hybrid Sort"],
        patch_artist=True,
        boxprops=dict(facecolor="lightblue"),
        medianprops=dict(color="red"),
    )

    plt.title("Merge Sort vs. Hybrid Sort Runtime Comparison (S=25, n=1E+7)")
    plt.ylabel("Run Time (ms)")
    plt.grid(True)

    # Save the plot as an image file
    plt.savefig(output_file)
    plt.show()


def main():
    # Read runtime data from stdin
    hybrid_sort_times, merge_sort_times = read_data_from_stdin()

    # Plot the boxplot and save it as an image
    plot_boxplot(hybrid_sort_times, merge_sort_times)


if __name__ == "__main__":
    main()
