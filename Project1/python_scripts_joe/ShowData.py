import sys
import matplotlib.pyplot as plt


def read_data_from_stdin():
    # Initialize lists to store input sizes and comparison counts
    input_sizes = []
    comparison_counts = []

    # Read data from stdin line by line
    for line in sys.stdin:
        try:
            # Split the line into input size and comparison count
            input_size, comparison_count = map(int, line.split())
            input_sizes.append(input_size)
            comparison_counts.append(comparison_count)
        except ValueError:
            # Skip lines that do not match the expected format
            print(f"Skipping invalid line: {line.strip()}", file=sys.stderr)

    return input_sizes, comparison_counts


def plot_graph(input_sizes, comparison_counts):
    plt.figure(figsize=(10, 6))
    plt.plot(input_sizes, comparison_counts, marker="o", linestyle="-", color="b")
    plt.xlabel("Input Size (n)")
    plt.ylabel("Comparison Count")
    plt.title("Input Size vs. Comparison Count")
    plt.grid(True)
    plt.show()


def main():
    # Read data from stdin
    input_sizes, comparison_counts = read_data_from_stdin()

    # Plot the graph
    plot_graph(input_sizes, comparison_counts)


if __name__ == "__main__":
    main()
