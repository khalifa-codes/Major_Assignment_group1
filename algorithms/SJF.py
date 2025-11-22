from typing import List, Dict, Tuple
import copy

def sjf(processes: List[Dict]) -> Tuple[List[Dict], List[Tuple[str, int, int]]]:
    # Input Validations
    if not isinstance(processes, list):
        raise TypeError("Processes must be provided as a list of dictionaries.")

    if not processes:
        return [], []

    required_keys = {"pid", "arrival", "burst"}

    for p in processes:
        if not required_keys.issubset(p.keys()):#checking required keys are present in each process list
            raise KeyError(f"Process {p} is missing required keys: {required_keys}")
        if p["arrival"] < 0 or p["burst"] <= 0: #this checks that arrival is not negative and burst is not negative also not equal to 0
            raise ValueError("Arrival must be >= 0 and Burst Time must be > 0.")

    # Preparing  Data
    processes = copy.deepcopy(processes)  # Avoid modifying original input
    completed = []
    gantt_chart = []
    current_time = 0
    # Make a shallow copy of the process list to keep track of processes that are not finished yet
    remaining_processes = processes.copy()

    # Main SJF Loop
    while remaining_processes:
        # Selecting processes that has arrived
        available = [p for p in remaining_processes if p["arrival"] <= current_time]#using list comprehension

        if not available:
            # CPU is free until next process arrives
            next_proc = min(remaining_processes, key=lambda x: x["arrival"])#if no processes available, cpu will find process with small arrival by default
            current_time = next_proc["arrival"]
            available = [next_proc]

        # picking process with shortest burst time
        proc = min(available, key=lambda x: x["burst"])

        # Recording start and finish times
        proc["start"] = current_time
        current_time += proc["burst"]
        proc["finish"] = current_time

        # Metrics 
        proc["turnaround"] = proc["finish"] - proc["arrival"]
        proc["waiting"] = proc["turnaround"] - proc["burst"]
        proc["response"] = proc["start"] - proc["arrival"]

        # Updating lists
        completed.append(proc)
        gantt_chart.append((proc["pid"], proc["start"], proc["finish"]))
        # Removes the completed process from the list of processes, which are still waiting to be scheduled
        remaining_processes.remove(proc)

    return completed, gantt_chart

if _name_ == "_main_":
    sample_processes = [
        {"pid": "P1", "arrival": 0, "burst": 6},
        {"pid": "P2", "arrival": 1, "burst": 8},
        {"pid": "P3", "arrival": 2, "burst": 7},
        {"pid": "P4", "arrival": 3, "burst": 3},
    ]

    print("\n" + "="*80)
    print(" " * 25 + "SJF SCHEDULING SIMULATOR")
    print("="*80)

    print("\nINPUT PROCESSES:")
    print("-"*80)
    print(f"{'PID':<8}{'Arrival Time':<15}{'Burst Time':<12}")
    print("-"*80)
    for p in sample_processes:
        print(f"{p['pid']:<11}{p['arrival']:<15}{p['burst']:<12}")
    print("-"*80)

    results, chart = sjf(sample_processes)

    # OUTPUT
    # Gantt Chart
    print("\nGANTT CHART:")
    execution_order = " → ".join([pid for pid, _, _ in chart])
    print(f"Execution Order: {execution_order}\n")
    timeline = "|"
    time_labels = "0"
    for pid, start, end in chart:
        timeline += f" {pid:^8} |"
        time_labels += f"{'':>8}{end:>3}"
    print(timeline)
    print(time_labels)

    # Process metrics
    print("\nPROCESS METRICS:")
    print("-"*80)
    print(f"{'PID':<8}{'Arrival':<10}{'Burst':<8}{'Start':<8}{'Finish':<8}"
          f"{'Waiting':<10}{'Turnaround':<12}{'Response':<10}")
    print("-"*80)
    for p in results:
        print(f"{p['pid']:<11}{p['arrival']:<9}{p['burst']:<8}{p['start']:<8}{p['finish']:<8}"
              f"{p['waiting']:<10}{p['turnaround']:<12}{p['response']:<10}")
    print("-"*80)

    # Average metrics
    avg_waiting = sum(p['waiting'] for p in results)/len(results)
    avg_turnaround = sum(p['turnaround'] for p in results)/len(results)
    print(f"\nAverage Waiting Time: {avg_waiting:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround:.2f}")
    print("="*80 + "\n")