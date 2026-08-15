"""
HPC DATA STRUCTURE OPTIMIZATION PROJECT

Optimization Technique:
    Data Structure Optimization and Data Locality

Project Objective:
    This program compares two different data structures:

    1. A singly linked list - the unoptimized implementation.
    2. A Python list - the optimized implementation.

    Both structures contain the same values and perform the same
    sequential summation operation.

    The purpose of the experiment is to investigate whether the
    organization of data affects execution performance.

    This project is based on the data-locality and data-structure
    optimization discussed in:

    Azad, M. A. K., Iqbal, N., Hassan, F., & Roy, P.
    "An Empirical Study of High Performance Computing (HPC)
    Performance Bugs."
"""

# ==============================================================
# IMPORT REQUIRED PYTHON MODULES
# ==============================================================

# The time module allows us to measure how long an operation takes.
# We use time.perf_counter() because it provides a high-resolution
# timer that is appropriate for measuring short execution times.
import time

# The statistics module allows us to calculate the average and
# standard deviation of multiple benchmark runs.
import statistics

# The csv module allows us to save our experimental results into
# a CSV file so that the results can later be used in the report
# or plotted as a graph.
import csv

# The gc module provides access to Python's garbage collector.
# We use it between experiments to reduce the effect of unused
# Python objects from previous experiments.
import gc


# ==============================================================
# LINKED LIST NODE
# ==============================================================

class Node:
    """
    This class represents one node in the linked list.

    Each node contains:
        - value: the actual data
        - next: a reference to the next node

    Unlike a contiguous array/list, linked-list nodes do not need
    to be stored next to each other in memory.
    """

    # __slots__ tells Python exactly which attributes each Node
    # object will contain. This reduces unnecessary object overhead.
    __slots__ = ("value", "next")

    def __init__(self, value):
        # Store the data value inside this node.
        self.value = value

        # Initially, this node does not point to another node.
        # The value is changed when another node is connected.
        self.next = None


# ==============================================================
# LINKED LIST DATA STRUCTURE
# ==============================================================

class LinkedList:
    """
    This class implements a simple singly linked list.

    The linked list is used as the unoptimized data structure
    in our experiment.
    """

    def __init__(self):

        # head stores the first node in the linked list.
        # It is None when the list is empty.
        self.head = None

        # tail stores the last node in the linked list.
        # Keeping a tail reference makes adding a new node
        # at the end of the list more efficient.
        self.tail = None

        # size keeps track of how many elements are in the list.
        self.size = 0

    def append(self, value):
        """
        Add one new value to the end of the linked list.
        """

        # Create a new Node object containing the value.
        new_node = Node(value)

        # If head is None, the linked list is currently empty.
        if self.head is None:

            # The new node becomes the first node.
            self.head = new_node

            # Because it is also the only node, it is the last node.
            self.tail = new_node

        else:

            # The current last node now points to the new node.
            self.tail.next = new_node

            # Update tail so that it points to the newly added node.
            self.tail = new_node

        # Increase the number of elements stored in the linked list.
        self.size += 1

    def sequential_sum(self):
        """
        Traverse every node and calculate the sum of its values.

        This represents the computational operation that will be
        compared with the optimized data structure.
        """

        # Start traversal at the first node.
        current = self.head

        # Start the total at zero before processing any values.
        total = 0

        # Continue until there are no more nodes.
        while current is not None:

            # Add the current node's value to the running total.
            total += current.value

            # Move to the next node using the stored reference.
            current = current.next

        # Return the final sum after traversing the entire list.
        return total


# ==============================================================
# CONTIGUOUS DATA STRUCTURE
# ==============================================================

def create_contiguous_list(values):
    """
    Create a Python list containing the same values.

    Python lists use a contiguous dynamic-array representation
    for their element references. This allows sequential access
    to follow a regular memory pattern.

    This represents the optimized data structure in our
    experiment.
    """

    # Convert the input sequence into a Python list.
    # The resulting list provides efficient sequential traversal.
    return list(values)


# ==============================================================
# SUM VALUES IN CONTIGUOUS LIST
# ==============================================================

def contiguous_sequential_sum(data):
    """
    Traverse the Python list sequentially and calculate the sum.

    We intentionally use an explicit loop instead of Python's
    built-in sum() function. This keeps the computational operation
    more comparable to the linked-list traversal.
    """

    # Initialize the total before beginning the traversal.
    total = 0

    # Visit each value sequentially from the beginning to the end.
    for value in data:

        # Add the current value to the running total.
        total += value

    # Return the completed sum.
    return total


# ==============================================================
# GENERATE TEST DATA
# ==============================================================

def generate_data(size):
    """
    Generate a predictable dataset containing integers from
    1 through the requested size.

    Using deterministic data ensures that both data structures
    receive exactly the same values.
    """

    # range() creates the sequence of numbers.
    # list() converts the sequence into a Python list.
    #
    # Example:
    # size = 5
    # generated values = [1, 2, 3, 4, 5]
    return list(range(1, size + 1))


# ==============================================================
# BUILD LINKED LIST
# ==============================================================

def build_linked_list(values):
    """
    Convert the input values into our linked-list structure.
    """

    # Create an empty linked list before adding any values.
    linked_list = LinkedList()

    # Process each value from the input dataset.
    for value in values:

        # Add the current value as a new linked-list node.
        linked_list.append(value)

    # Return the completed linked list.
    return linked_list


# ==============================================================
# BENCHMARK FUNCTION
# ==============================================================

def benchmark(function, repetitions=5):
    """
    Measure the execution time of a function multiple times.

    Running the function several times is important because a
    single timing measurement can be affected by background
    operating-system activity or other temporary factors.

    Returns:
        average_time
        minimum_time
        standard_deviation
        result
    """

    # Create an empty list that will store the runtime of
    # every benchmark iteration.
    times = []

    # Store the function's calculated result so we can verify
    # that both implementations produce the same answer.
    result = None

    # ----------------------------------------------------------
    # WARM-UP RUN
    # ----------------------------------------------------------

    # Run the function once before collecting timing results.
    # This warm-up helps avoid treating the first execution as
    # representative when the program is still initializing.
    result = function()

    # ----------------------------------------------------------
    # TIMED RUNS
    # ----------------------------------------------------------

    # Repeat the benchmark several times.
    for iteration in range(repetitions):

        # Record the exact starting time immediately before
        # executing the operation.
        start_time = time.perf_counter()

        # Execute the operation being tested.
        result = function()

        # Record the time immediately after the operation finishes.
        end_time = time.perf_counter()

        # Calculate the elapsed time for this iteration.
        elapsed_time = end_time - start_time

        # Store this measurement so it can be analyzed later.
        times.append(elapsed_time)

    # Calculate the average execution time across all runs.
    average_time = statistics.mean(times)

    # The minimum time represents the fastest observed execution.
    minimum_time = min(times)

    # Calculate standard deviation to show timing variability.
    if len(times) > 1:
        standard_deviation = statistics.stdev(times)
    else:
        standard_deviation = 0

    # Return all benchmark information to the calling function.
    return (
        average_time,
        minimum_time,
        standard_deviation,
        result
    )


# ==============================================================
# RUN ONE EXPERIMENT
# ==============================================================

def run_experiment(size, repetitions=5):
    """
    Run the complete comparison for one dataset size.

    The same values are placed into both data structures.
    Both structures then perform the same summation operation.
    """

    print("\n" + "=" * 75)

    # Display the size currently being tested.
    print(f"DATASET SIZE: {size:,} ELEMENTS")

    print("=" * 75)

    # ----------------------------------------------------------
    # STEP 1: GENERATE DATA
    # ----------------------------------------------------------

    print("Step 1: Generating test data...")

    # Create the dataset that will be used by both implementations.
    values = generate_data(size)

    # ----------------------------------------------------------
    # STEP 2: CREATE LINKED LIST
    # ----------------------------------------------------------

    print("Step 2: Creating linked-list data structure...")

    # Convert the generated values into a linked list.
    # This is our unoptimized data structure.
    linked_list = build_linked_list(values)

    # ----------------------------------------------------------
    # STEP 3: CREATE CONTIGUOUS LIST
    # ----------------------------------------------------------

    print("Step 3: Creating contiguous Python list...")

    # Create the optimized data structure using a Python list.
    contiguous_list = create_contiguous_list(values)

    # ----------------------------------------------------------
    # STEP 4: CALCULATE EXPECTED RESULT
    # ----------------------------------------------------------

    # The sum of integers from 1 to n can be calculated using
    # the mathematical formula:
    #
    # n(n + 1) / 2
    #
    # We use this value to verify that both implementations
    # produce the correct answer.
    expected_sum = size * (size + 1) // 2

    # ----------------------------------------------------------
    # STEP 5: BENCHMARK LINKED LIST
    # ----------------------------------------------------------

    print("Step 4: Benchmarking linked-list traversal...")

    # Measure the time required to sequentially traverse
    # and sum all elements in the linked list.
    (
        linked_average,
        linked_minimum,
        linked_std,
        linked_result
    ) = benchmark(
        linked_list.sequential_sum,
        repetitions
    )

    # ----------------------------------------------------------
    # STEP 6: BENCHMARK CONTIGUOUS LIST
    # ----------------------------------------------------------

    print("Step 5: Benchmarking contiguous-list traversal...")

    # Measure the time required to sequentially traverse
    # and sum all elements in the Python list.
    (
        list_average,
        list_minimum,
        list_std,
        list_result
    ) = benchmark(
        lambda: contiguous_sequential_sum(contiguous_list),
        repetitions
    )

    # ----------------------------------------------------------
    # STEP 7: VERIFY CORRECTNESS
    # ----------------------------------------------------------

    print("Step 6: Verifying calculation results...")

    # Verify that the linked-list result is correct.
    if linked_result != expected_sum:
        raise ValueError(
            "ERROR: Linked-list calculation produced an "
            "incorrect result."
        )

    # Verify that the contiguous-list result is correct.
    if list_result != expected_sum:
        raise ValueError(
            "ERROR: Contiguous-list calculation produced an "
            "incorrect result."
        )

    # Verify that both implementations produced the same result.
    if linked_result != list_result:
        raise ValueError(
            "ERROR: The two implementations produced "
            "different results."
        )

    # ----------------------------------------------------------
    # STEP 8: CALCULATE SPEEDUP
    # ----------------------------------------------------------

    # Speedup compares the runtime of the unoptimized version
    # with the runtime of the optimized version.
    #
    # Formula:
    #
    # Speedup = Unoptimized Time / Optimized Time
    #
    # A value greater than 1 means that the optimized version
    # executed faster.
    speedup = linked_average / list_average

    # Calculate the percentage reduction in execution time.
    #
    # Formula:
    #
    # ((Old Time - New Time) / Old Time) * 100
    #
    execution_reduction = (
        (linked_average - list_average)
        / linked_average
    ) * 100

    # ----------------------------------------------------------
    # STEP 9: DISPLAY RESULTS
    # ----------------------------------------------------------

    print("\nRESULTS")
    print("-" * 75)

    print(f"Expected sum:              {expected_sum:,}")
    print(f"Linked-list result:        {linked_result:,}")
    print(f"Contiguous-list result:    {list_result:,}")

    print("\nExecution Time")
    print("-" * 75)

    print(
        f"Linked-list average:       "
        f"{linked_average:.6f} seconds"
    )

    print(
        f"Linked-list minimum:       "
        f"{linked_minimum:.6f} seconds"
    )

    print(
        f"Linked-list std. deviation:"
        f" {linked_std:.6f} seconds"
    )

    print()

    print(
        f"Contiguous-list average:   "
        f"{list_average:.6f} seconds"
    )

    print(
        f"Contiguous-list minimum:   "
        f"{list_minimum:.6f} seconds"
    )

    print(
        f"Contiguous-list std. dev.: "
        f"{list_std:.6f} seconds"
    )

    print("\nOptimization Analysis")
    print("-" * 75)

    print(f"Speedup:                   {speedup:.2f}x")

    print(
        f"Execution-time reduction:  "
        f"{execution_reduction:.2f}%"
    )

    # ----------------------------------------------------------
    # STEP 10: RETURN RESULTS
    # ----------------------------------------------------------

    # Return all measurements so they can be stored in the
    # final results table and CSV file.
    return {
        "dataset_size": size,
        "linked_average": linked_average,
        "linked_minimum": linked_minimum,
        "linked_std": linked_std,
        "contiguous_average": list_average,
        "contiguous_minimum": list_minimum,
        "contiguous_std": list_std,
        "speedup": speedup,
        "execution_reduction": execution_reduction
    }


# ==============================================================
# RUN ALL EXPERIMENTS
# ==============================================================

def run_all_experiments():
    """
    Run the experiment using multiple dataset sizes.

    Testing multiple sizes allows us to determine whether the
    performance difference changes as the amount of data increases.
    """

    # These dataset sizes provide a range of small-to-large
    # experiments without requiring external libraries.
    dataset_sizes = [
        100_000,
        250_000,
        500_000,
        1_000_000
    ]

    # Each test will be repeated five times.
    repetitions = 5

    # Store the results from every dataset size.
    all_results = []

    print("\n")
    print("*" * 75)
    print("HIGH-PERFORMANCE COMPUTING")
    print("DATA STRUCTURE OPTIMIZATION EXPERIMENT")
    print("*" * 75)

    print("\nOptimization technique:")
    print("Data Structure Optimization / Data Locality")

    print("\nUnoptimized data structure:")
    print("Singly Linked List")

    print("\nOptimized data structure:")
    print("Contiguous Python List")

    print("\nBenchmark operation:")
    print("Sequential traversal and summation")

    print("\nNumber of timing repetitions:")
    print(repetitions)

    # ----------------------------------------------------------
    # RUN EACH DATASET SIZE
    # ----------------------------------------------------------

    for size in dataset_sizes:

        # Run the experiment for the current dataset size.
        result = run_experiment(
            size,
            repetitions
        )

        # Store the result so we can create a final summary.
        all_results.append(result)

        # Run garbage collection before starting the next
        # experiment to clean up objects that are no longer used.
        gc.collect()

    # Return all experimental results.
    return all_results


# ==============================================================
# SAVE RESULTS TO CSV
# ==============================================================

def save_results(results, filename="hpc_optimization_results.csv"):
    """
    Save all benchmark results to a CSV file.

    Saving the results allows the data to be imported into
    Excel, Tableau, Python, or another visualization tool.
    """

    # Define the column names that will appear in the CSV file.
    fieldnames = [
        "dataset_size",
        "linked_average",
        "linked_minimum",
        "linked_std",
        "contiguous_average",
        "contiguous_minimum",
        "contiguous_std",
        "speedup",
        "execution_reduction"
    ]

    # Open the output CSV file in write mode.
    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as csv_file:

        # Create a CSV writer using the column names defined above.
        writer = csv.DictWriter(
            csv_file,
            fieldnames=fieldnames
        )

        # Write the column headers first.
        writer.writeheader()

        # Write one row for every dataset-size experiment.
        for result in results:

            # Add the current experiment's measurements to the CSV.
            writer.writerow(result)

    print("\n")
    print("=" * 75)
    print(f"Results saved successfully to: {filename}")
    print("=" * 75)


# ==============================================================
# DISPLAY FINAL SUMMARY
# ==============================================================

def print_summary(results):
    """
    Display all experimental results in a readable table.
    """

    print("\n")
    print("=" * 95)
    print("FINAL PERFORMANCE SUMMARY")
    print("=" * 95)

    # Print the table header.
    print(
        f"{'Dataset Size':>15}"
        f"{'Linked List':>18}"
        f"{'Contiguous List':>20}"
        f"{'Speedup':>15}"
        f"{'Time Reduction':>20}"
    )

    print("-" * 95)

    # Print one row for every experiment.
    for result in results:

        print(
            f"{result['dataset_size']:>15,}"
            f"{result['linked_average']:>18.6f}"
            f"{result['contiguous_average']:>20.6f}"
            f"{result['speedup']:>14.2f}x"
            f"{result['execution_reduction']:>19.2f}%"
        )

    print("=" * 95)


# ==============================================================
# MAIN PROGRAM
# ==============================================================

def main():
    """
    Main function that controls the entire experiment.

    The program follows these major steps:

        1. Generate test data.
        2. Create the linked-list implementation.
        3. Create the contiguous-list implementation.
        4. Benchmark both implementations.
        5. Verify that both produce the same answer.
        6. Calculate speedup.
        7. Display the results.
        8. Save results to a CSV file.
    """

    # Print the project title when the program starts.
    print("\n")
    print("*" * 75)
    print("HPC DATA STRUCTURE OPTIMIZATION PROJECT")
    print("*" * 75)

    # Explain the selected optimization technique.
    print("\nSelected optimization:")
    print("Data Structure Optimization through Data Locality")

    # Explain which implementation represents the original
    # or unoptimized approach.
    print("\nUnoptimized implementation:")
    print("Singly Linked List")

    # Explain which implementation represents the optimized
    # approach.
    print("\nOptimized implementation:")
    print("Contiguous Python List")

    # Explain what is being measured.
    print("\nPerformance measurement:")
    print("Sequential traversal and summation")

    # ----------------------------------------------------------
    # EXECUTE EXPERIMENTS
    # ----------------------------------------------------------

    # Run all dataset-size experiments.
    results = run_all_experiments()

    # ----------------------------------------------------------
    # DISPLAY FINAL RESULTS
    # ----------------------------------------------------------

    # Display the complete comparison table.
    print_summary(results)

    # ----------------------------------------------------------
    # SAVE RESULTS
    # ----------------------------------------------------------

    # Save the experimental results so they can be used in
    # the project report and performance visualization.
    save_results(results)

        # Print a final confirmation message.
    print("\nExperiment completed successfully.")

    print("\nGenerated output file:")
    print("hpc_optimization_results.csv")


# ==============================================================
# PROGRAM ENTRY POINT
# ==============================================================

# This condition checks whether this Python file is being
# executed directly by the user.
#
# When the condition is True, the main() function is called
# and the complete experiment begins.


# ==============================================================
# PROGRAM ENTRY POINT
# ==============================================================

# Python sets __name__ to "__main__" when this file is executed
# directly rather than imported by another Python program.
#
# This condition ensures that main() runs only when the user
# executes this file directly.
if __name__ == "__main__":

    # Start the HPC data structure optimization experiment.
    main()
