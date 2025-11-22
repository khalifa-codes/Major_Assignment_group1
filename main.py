# main.py
"""
CPU Scheduling Simulator (CLI)
------------------------------
This program runs and compares CPU scheduling algorithms:
- FCFS (First Come First Serve)
- SJF (Shortest Job First)
- RR  (Round Robin)

Includes:
- Gantt chart visualization
- Process metrics (WT, TAT, Response)
- Comparative analysis
"""

from typing import List, Dict
from copy import deepcopy
import sys

from algorithms import fcfs, sjf, round_robin
from utils import average_waiting_time, average_turnaround_time, print_gantt_chart
from advance_features import bankers_algorithm
from advance_features import total_resources, allocation, max_need, process_ids, resource_names


# ---------------------------------------------
# OUTPUT FUNCTIONS
# ---------------------------------------------
def display_processes(processes: List[Dict]):
    """Display the input processes in tabular form."""
    print(f"{'PID':<8} {'Arrival':<10} {'Burst':<10} {'Priority':<10}")
    print("-" * 45)
    for p in processes:
        priority = p.get('priority', '-')
        print(f"{p['pid']:<8} {p['arrival']:<10} {p['burst']:<10} {priority:<10}")
    print("-" * 45)


def display_metrics(results: List[Dict]):
    """Display metrics for each process and averages."""
    print(f"{'PID':<8} {'Waiting Time':<15} {'Turnaround Time':<18} {'Response Time':<15}")
    print("-" * 60)
    for p in results:
        print(f"{p['pid']:<8} {p['waiting']:<15} {p['turnaround']:<18} {p['response']:<15}")
    print("-" * 60)
    avg_wt = average_waiting_time(results)
    avg_tat = average_turnaround_time(results)
    print(f"\nAverage Waiting Time   : {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")
    print("-" * 60)
    return avg_wt, avg_tat  # Return for comparative analysis


def run_algorithm(name: str, func, processes: List[Dict], **kwargs):
    """Run an algorithm, display Gantt chart and metrics."""
    print("\n" + "=" * 80)
    print(f"{' ' * 25}{name} RESULTS")
    print("=" * 80 + "\n")
    proc_copy = deepcopy(processes)
    results, chart = func(proc_copy, **kwargs) if kwargs else func(proc_copy)
    print("GANTT CHART:")
    print_gantt_chart(chart)
    print("\nPROCESS METRICS:")
    avg_wt, avg_tat = display_metrics(results)
    return results, avg_wt, avg_tat


# ---------------------------------------------
# COMPARATIVE ANALYSIS FUNCTION
# ---------------------------------------------
def comparative_analysis(all_results: List[Dict]):
    """Display side-by-side comparison of all three algorithms."""
    print("\n" + "=" * 80)
    print(" " * 20 + "COMPARATIVE ANALYSIS OF ALGORITHMS")
    print("=" * 80)
    print(f"{'Algorithm':<14} {'Avg WT':<17} {'Avg TAT':<14}")
    print("-" * 45)

    for alg in all_results:
        bar_wt = "█" * int(round(alg['avg_wt'] ))
        bar_tat = "█" * int(round(alg['avg_tat'] ))
        print(f"{alg['name']:<14} {alg['avg_wt']:<4.2f} {bar_wt:<12} {alg['avg_tat']:<4.2f} {bar_tat}\n")
    print("-" * 40)

    # Highlight best metrics
    best_wt = min(all_results, key=lambda x: x['avg_wt'])
    best_tat = min(all_results, key=lambda x: x['avg_tat'])
    print(f"\nBest Average Waiting Time   : {best_wt['name']}")
    print(f"Best Average Turnaround Time: {best_tat['name']}")
    print("-" * 80)


# ---------------------------------------------
# FUNCTION TO GET USER INPUT PROCESSES
# ---------------------------------------------
def input_processes() -> List[Dict]:
    """Prompt user to enter processes for an algorithm."""
    processes = []
    try:
        n = int(input("Enter number of processes: "))
    except ValueError:
        print("Invalid number! Defaulting to 3 processes.")
        n = 3
    for i in range(n):
        pid = input(f"Enter PID for process {i+1}: ").upper()
        try:
            arrival = int(input(f"Arrival time for {pid}: "))
            burst = int(input(f"Burst time for {pid}: "))
            priority_input = input(f"Priority for {pid} (optional, press enter to skip): ")
            priority = int(priority_input) if priority_input.strip() != "" else 0
        except ValueError:
            print("Invalid input! Setting numeric values to default 0.")
            arrival, burst, priority = 0, 1, 0
        processes.append({
            "pid": pid,
            "arrival": arrival,
            "burst": burst,
            "priority": priority
        })
    return processes


# ---------------------------------------------
# MAIN FUNCTION
# ---------------------------------------------
def main():
    executed_algorithms = {}
    algo_name = ["FCFS","SJF","RR"]

    while True:
        print("\n" + "=" * 80)
        print(" " * 25 + "CPU SCHEDULING SIMULATOR")
        print("=" * 80 + "\n")
        print(f"1.Run FCFS\n2.Run SJF\n3.Run RR\n4.Comparative Analysis\n5.Deadlock Prevention (Banker's algorithm)\n6.Exit")
        try:
            choice = int(input("Enter choice (1-6): "))
        except ValueError:
            print("\nInvalid input! Enter a number between 1-6.\n")
            continue
        
        if choice in [1, 2, 3]:
            print(f"\nEnter processes for algorithm {algo_name[choice -1]}:")
            user_processes = input_processes()
            display_processes(user_processes)

        if choice == 1:
            print("\nRunning First Come First Serve...\n")
            results, avg_wt, avg_tat = run_algorithm("FCFS", fcfs, user_processes)
            executed_algorithms['FCFS'] = {'results': results, 'avg_wt': avg_wt, 'avg_tat': avg_tat}

        elif choice == 2:
            print("\nRunning Shortest Job First...\n")
            results, avg_wt, avg_tat = run_algorithm("SJF", sjf, user_processes)
            executed_algorithms['SJF'] = {'results': results, 'avg_wt': avg_wt, 'avg_tat': avg_tat}

        elif choice == 3:
            print("\nRunning Round Robin...\n")
            try:
                time_quantum = int(input("Enter Time Quantum for Round Robin: "))
                if time_quantum <= 0:
                    print("Time Quantum must be positive. Defaulting to 2.")
                    time_quantum = 2
            except ValueError:
                print("Invalid input! Defaulting Time Quantum to 2.")
                time_quantum = 2
            results, avg_wt, avg_tat = run_algorithm("RR", round_robin, user_processes, quantum=time_quantum) 
            executed_algorithms['RR'] = {'results': results, 'avg_wt': avg_wt, 'avg_tat': avg_tat}
        elif choice == 4:
            print("\nRunning Comparative Analysis...\n")
            if set(executed_algorithms.keys()) == {'FCFS', 'SJF', 'RR'}:
                all_results = []
                for name in ['FCFS', 'SJF', 'RR']:
                    data = executed_algorithms[name]
                    all_results.append({
                        'name': name,
                        'avg_wt': data['avg_wt'],
                        'avg_tat': data['avg_tat']
                    })
                comparative_analysis(all_results)
            else:
                print("\nComparative analysis requires all three algorithms to be run first!\n")
                print("   Run FCFS, SJF, and RR before selecting this option.\n")

        elif choice == 5:
            print("\nRunning Deadlock Prevention (Banker's Algorithm)...\n")
            bankers_algorithm(
            total_resources=total_resources,
            allocation=allocation,
            max_need=max_need,
            process_ids=process_ids,
            resource_names=resource_names
    )
        elif choice == 6:
            print("\nGoodbye! Thanks for using CPU Scheduling Simulator.\n")
            sys.exit(0)
        else:
            print("\n Choice must be between 1-6!\n")


# ---------------------------------------------
# ENTRY POINT
# ---------------------------------------------
if __name__ == "__main__":
    main()
