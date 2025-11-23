from .Bankers_data import total_resources, allocation, max_need, process_ids, resource_names
def Bankers_algorithm(total_resources, allocation, max_need, process_ids, resource_names):
    """
    Implements Banker's Algorithm for deadlock prevention.
    """

    num_resources = len(resource_names)
    # Calculate Available = Total - Σ Allocation
    allocated_sum = [sum(x[i] for x in allocation) for i in range(num_resources)]
    available = [total_resources[i] - allocated_sum[i] for i in range(num_resources)]

    # Calculate Need = Max - Allocation
    need = [
        [max_need[i][j] - allocation[i][j] for j in range(num_resources)]
        for i in range(len(allocation))
    ]

    finished = [False] * len(process_ids)
    safe_sequence = []

    print("\n===================== DEADLOCK PREVENTION: BANKER'S ALGORITHM =====================\n")

    print("Total Resources:")
    for i in range(num_resources):
        print(f"{resource_names[i]} = {total_resources[i]}", end="  ")
    print("\n")

    # Process Details Table
    print("PROCESS DETAILS:")
    header_alloc = "Allocation(" + ",".join(resource_names) + ")"
    header_max = "Max Need(" + ",".join(resource_names) + ")"
    header_need = "Remaining Need"
    print(f"{'PID':<8} {header_alloc:<25} {header_max:<25} {header_need:<20} Status")
    print("-"*90)
    for i, pid in enumerate(process_ids):
        print(f"{pid:<8} {str(allocation[i]):<25} {str(max_need[i]):<25} {str(need[i]):<20} Pending")
    print()

    # Available Resources
    print("AVAILABLE RESOURCES:")
    for i in range(num_resources):
        print(f"{resource_names[i]} = {available[i]}", end="  ")
    print("\n" + "-"*90)

    # --- Banker's Algorithm Logic ---
    while len(safe_sequence) < len(process_ids):

        executed_in_cycle = False

        for i in range(len(process_ids)):
            if not finished[i]:
                # Check if Need <= Available
                if all(need[i][r] <= available[r] for r in range(num_resources)):
                    print(f"Process {process_ids[i]} can finish. Releasing resources: {allocation[i]}")
                    # Release resources
                    available = [available[r] + allocation[i][r] for r in range(num_resources)]
                    finished[i] = True
                    safe_sequence.append(process_ids[i])
                    executed_in_cycle = True

                    print("New Available: ", end="")
                    print(", ".join([f"{resource_names[r]}={available[r]}" for r in range(num_resources)]), "\n")
        
        if not executed_in_cycle:
            print("SYSTEM STATE: UNSAFE — No safe sequence exists.\n")
            return None

    # Final Output
    print("-"*90)
    print("SAFE SEQUENCE FOUND:")
    print(" → ".join(safe_sequence))
    print("\nSYSTEM STATE: SAFE")
    print("="*90 + "\n")

    return safe_sequence


if __name__ == "__main__":
    Bankers_algorithm(total_resources, allocation, max_need, process_ids, resource_names)
